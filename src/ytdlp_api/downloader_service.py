import os
import shutil
import tempfile

from fastapi import HTTPException
from yt_dlp import YoutubeDL

from .DownloadRequest import DownloadRequest, VIDEO_FORMATS, VIDEO_QUALITY_FORMATS, AUDIO_FORMATS

SECRET_COOKIE_FILE = os.environ.get("YTDLP_COOKIE_FILE", "/etc/secrets/cookies.txt")
_writable_cookie_file = None


def get_cookie_file() -> str | None:
    global _writable_cookie_file

    if _writable_cookie_file is not None:
        return _writable_cookie_file

    if not os.path.isfile(SECRET_COOKIE_FILE):
        print(
            f"yt-dlp cookies not found at {SECRET_COOKIE_FILE}. "
            "Requests will run without authentication."
        )
        return None

    if os.path.getsize(SECRET_COOKIE_FILE) == 0:
        print(f"yt-dlp cookie file is empty: {SECRET_COOKIE_FILE}")
        return None

    tmp_dir = tempfile.mkdtemp(prefix="cookies_")
    dest = os.path.join(tmp_dir, "cookies.txt")
    shutil.copy(SECRET_COOKIE_FILE, dest)
    _writable_cookie_file = dest

    print(f"yt-dlp cookies loaded from {SECRET_COOKIE_FILE}")
    return _writable_cookie_file


def base_ydl_opts() -> dict:
    opts = {
        'verbose': True,
        # Web is the client that supports the browser cookies exported for Render.
        'extractor_args': {'youtube': {'player_client': ['web']}},
    }

    cookie_file = get_cookie_file()

    if cookie_file:
        opts["cookiefile"] = cookie_file

    return opts

def verify_correct_format(download_type: str, file_format: str) -> None:
    if download_type == "video" and file_format in VIDEO_FORMATS:
        return

    if download_type == "audio" and file_format in AUDIO_FORMATS:
        return

    raise HTTPException(
        status_code=400,
        detail=f"Invalid format '{file_format}' for download type '{download_type}'."
    )


def cleanup_files(work_dir: str) -> None:
    if not work_dir:
        return

    try:
        shutil.rmtree(work_dir, ignore_errors=True)
        print(f"Server cleanup: {work_dir} removed.")
    except Exception as e:
        print(f"It could not be deleted {work_dir}: {e}")


def build_audio_opts(request: DownloadRequest) -> dict:
    verify_correct_format(request.download_type, request.file_format)

    opts = base_ydl_opts()
    opts.update({
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': request.file_format,
            'preferredquality': '192',
        }],
    })
    return opts


def build_video_opts(request: DownloadRequest) -> dict:
    verify_correct_format(request.download_type, request.file_format)

    if request.quality.lower() == "best":
        format_selector = "bestvideo+bestaudio/best"
    else:
        try:
            selected_quality_int = int(request.quality)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid quality value '{request.quality}'.")

        if selected_quality_int not in VIDEO_QUALITY_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid quality '{selected_quality_int}'. Allowed values: {VIDEO_QUALITY_FORMATS}."
            )

        info_url = get_youtube_url_info(request.url)
        max_quality_int = int(info_url.get("height") or 0)

        if max_quality_int > 0 and selected_quality_int <= max_quality_int:
            format_selector = f"bestvideo[height<={selected_quality_int}]+bestaudio/best[height<={selected_quality_int}]"
        else:
            format_selector = "bestvideo+bestaudio/best"

    opts = base_ydl_opts()
    opts.update({
        'format': format_selector,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': request.file_format,
        }],
    })
    return opts


def add_metadata_config(ydl_opts: dict) -> dict:
    ydl_opts.setdefault('postprocessors', [])
    ydl_opts['writethumbnail'] = True

    ydl_opts['postprocessors'].append({'key': 'FFmpegMetadata'})
    ydl_opts['postprocessors'].append({'key': 'FFmpegThumbnailsConvertor', 'format': 'jpg'})
    ydl_opts['postprocessors'].append({'key': 'EmbedThumbnail'})

    return ydl_opts


def process_youtube_download(request: DownloadRequest) -> tuple[str, str]:
    work_dir = tempfile.mkdtemp(prefix="ytdl_")

    try:
        if request.download_type == "audio":
            ydl_opts = build_audio_opts(request)
        else:
            ydl_opts = build_video_opts(request)

        ydl_opts['outtmpl'] = os.path.join(work_dir, '%(title)s.%(ext)s')

        if request.metadata:
            ydl_opts = add_metadata_config(ydl_opts)

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            raw_filename = ydl.prepare_filename(info)
            base_name = os.path.splitext(raw_filename)[0]
            generated_filename = base_name + f".{request.file_format}"

            if not os.path.exists(generated_filename):
                raise HTTPException(status_code=400, detail="The file could not be generated.")

        return generated_filename, work_dir

    except HTTPException:
        cleanup_files(work_dir)
        raise

    except Exception as e:
        cleanup_files(work_dir)
        raise HTTPException(status_code=400, detail=f"Error processing download: {str(e)}")


def get_youtube_url_info(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="No valid URL was provided")

    try:
        with YoutubeDL(base_ydl_opts()) as ydl:
            info = ydl.extract_info(url, download=False)
            return ydl.sanitize_info(info)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing URL information: {str(e)}")