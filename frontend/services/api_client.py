import requests

url_raw = "http://127.0.0.1:8000/api"

def get_video_info(url: str):
    payload:dict = {"url": url}
    
    response = requests.post(f"{url_raw}/url_info", json=payload)
    return response

def download_media(request: dict):
    response = requests.post(f"{url_raw}/download", json=request)
    return response

def start_download(request: dict):
    response = requests.post(f"{url_raw}/download/start", json=request)
    return response


def get_download_progress(job_id: str):
    response = requests.get(f"{url_raw}/download/progress/{job_id}")
    return response


def get_download_file(job_id: str):
    response = requests.get(f"{url_raw}/download/file/{job_id}")
    return response