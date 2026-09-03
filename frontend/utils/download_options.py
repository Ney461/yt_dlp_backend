VIDEO_FORMATS = ("mp4", "mkv", "mov")
AUDIO_FORMATS = ("m4a", "mp3", "flac", "opus")
VIDEO_QUALITY_FORMATS = (144, 240, 360, 480, 720, 1080, 1440, 2160, 4320)

def get_available_qualities(max_height):
    if not max_height:
        return [str(q) for q in VIDEO_QUALITY_FORMATS]

    filtered = [q for q in VIDEO_QUALITY_FORMATS if q <= max_height]

    if not filtered:
        filtered = [VIDEO_QUALITY_FORMATS[0]]

    return [str(q) for q in filtered]