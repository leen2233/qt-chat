import os
from typing import Optional

MEDIA_DIR = "/tmp/veia/"
os.makedirs(MEDIA_DIR, exist_ok=True)

def check_media_if_exists(filename: str) -> Optional[str]:
    path = os.path.join(MEDIA_DIR, filename)
    if os.path.exists(path):
        return path
    else:
        return None

def get_absolute_path(filename: str) -> str:
    return os.path.join(MEDIA_DIR, filename)
