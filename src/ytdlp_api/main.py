import os
import uuid

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool

from .download_request import DownloadRequest, InfoUrlRequest, VideoInfoResponse
from .downloader_service import (
    JOBS,
    cleanup_files,
    get_youtube_url_info,
    process_youtube_download,
    update_job_error,
)

PATH = "/api"

app = FastAPI()


@app.get(PATH + "/")
def read_root():
    return {"API WORKS!!!"}


@app.post(PATH + "/download/start")
def start_download(request: DownloadRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "starting", "percent": 0}

    background_tasks.add_task(run_download_job, job_id, request)

    return {"job_id": job_id}


def run_download_job(job_id: str, request: DownloadRequest) -> None:
    try:
        process_youtube_download(request, job_id=job_id)
    except Exception as error:
        update_job_error(job_id, getattr(error, "detail", error))


@app.get(PATH + "/download/progress/{job_id}")
def get_download_progress(job_id: str):
    job = JOBS.get(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job


@app.get(PATH + "/download/file/{job_id}")
def get_download_file(job_id: str, background_tasks: BackgroundTasks):
    job = JOBS.get(job_id)

    if not job or job.get("status") != "finished":
        raise HTTPException(status_code=400, detail="File not ready")

    filename = job["filename"]
    work_dir = job["work_dir"]

    background_tasks.add_task(cleanup_files, work_dir)
    background_tasks.add_task(JOBS.pop, job_id, None)

    return FileResponse(
        path=filename,
        filename=os.path.basename(filename),
        media_type="application/octet-stream"
    )

@app.post(PATH + "/download")
async def download(request: DownloadRequest, background_tasks: BackgroundTasks):
    generated_filename, work_dir = await run_in_threadpool(process_youtube_download, request)

    background_tasks.add_task(cleanup_files, work_dir)

    return FileResponse(
        path=generated_filename,
        filename=os.path.basename(generated_filename),
        media_type="application/octet-stream"
    )


@app.post(PATH + "/url_info", response_model=VideoInfoResponse)
def get_url_info(request: InfoUrlRequest):
    return get_youtube_url_info(request.url)