import logging
import os.path
import platform
import sys
from typing import Optional

import coverpy
import requests.exceptions

cover_py = coverpy.CoverPy()

# Possible values: "Darwin", "Windows"
ostype = platform.system()


# Get script/app path
if hasattr(sys, "frozen") and sys.frozen in ("windows_exe", "console_exe"):
    path = os.path.dirname(os.path.abspath(sys.executable))
else:
    path = os.path.dirname(__file__)

# Logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
)

log = logging.getLogger("applemusicrp")


def get_cover_art_url(title: str, artist: str, album: str) -> Optional[str]:
    """Get 512x512 cover art from the iTunes API"""
    try:
        result = cover_py.get_cover(f"{title} {artist} {album}", 1)
        return result.artwork(512)
    except (coverpy.exceptions.NoResultsException, requests.exceptions.HTTPError):
        return
