from typing import Literal, Optional

from pydantic import BaseModel


class DownloadRequest(BaseModel):
    url: str
    download_type: Literal["video", "audio"] = "video"
    quality: str = "best"
    metadata: bool = False
    file_format: Literal["mp4", "mkv", "mov", "m4a", "mp3", "flac", "opus"] = "mp4"
    
class InfoUrlRequest(BaseModel):
    url: str
    
class VideoInfoResponse(BaseModel):
    title: str
    duration: int
    max_height: Optional[int]
    thumbnail: Optional[str]    


VIDEO_FORMATS = ("mp4", "mkv", "mov")
AUDIO_FORMATS = ("m4a", "mp3", "flac", "opus")
VIDEO_QUALITY_FORMATS = (144, 240, 360, 480, 720, 1080, 1440, 2160, 4320)