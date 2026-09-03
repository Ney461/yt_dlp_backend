import os

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool

from .download_request import DownloadRequest, InfoUrlRequest
from .downloader_service import process_youtube_download, cleanup_files, get_youtube_url_info

PATH = "/api"

app = FastAPI()


@app.get(PATH + "/")
def read_root():
    return {"API WORKS!!!"}


@app.post(PATH + "/download")
async def download(request: DownloadRequest, background_tasks: BackgroundTasks):
    generated_filename, work_dir = await run_in_threadpool(process_youtube_download, request)

    background_tasks.add_task(cleanup_files, work_dir)

    return FileResponse(
        path=generated_filename,
        filename=os.path.basename(generated_filename),
        media_type="application/octet-stream"
    )


@app.post(PATH + "/url_info")
def get_url_info(request: InfoUrlRequest):
    return get_youtube_url_info(request.url)