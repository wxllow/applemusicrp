import os
import platform
import subprocess
import time
from sys import exit

import dialite
import pypresence.exceptions
from pypresence import Presence

from .config import Config
from .utils import get_cover_art_url, log, ostype, path

config = Config()

# OS-specific code
if ostype == "Darwin":
    macos_ver = platform.mac_ver()[0]

    macos_legacy = bool(
        int(platform.mac_ver()[0].split(".")[0]) < 10
        and int(platform.mac_ver()[0].split(".")[1]) < 15
    )
else:
    import pythoncom
    import win32com.client


# Initiate RPC
client_id = config.config.get("client_id", "952320054870020146")  # Client ID
RPC = Presence(client_id)  # Initialize the Presence client


def connect():
    RPC.connect()


def get_music_info():
    if ostype == "Darwin":
        # Get info using AppleScript and then parse
        if macos_legacy:
            # Legacy script for pre-catalina macOS
            script_loc = os.path.join(
                path, "scripts", "getmusicinfo-legacy.applescript"
            )
        else:
            # Normal script for macOS
            script_loc = os.path.join(path, "scripts", "getmusicinfo.applescript")

        p = subprocess.Popen(["osascript", script_loc], stdout=subprocess.PIPE)

        return p.stdout.read().decode("utf-8").strip().split("\\")
    else:
        # Check if iTunes is running
        itunes = win32com.client.GetActiveObject("iTunes.Application")

        # Get info using Windows API
        current_track = itunes.CurrentTrack
        playerstate = itunes.PlayerState

        if not current_track:
            return ["STOPPED"]

        return [
            ("PAUSED" if playerstate == 0 else "PLAYING"),
            current_track.Name,
            current_track.Artist,
            current_track.Album,
            str(itunes.PlayerPosition),
        ]


def get_rp(info, statuses):
    """Get additional Rich Presence data"""
    # .split(',')[0] is an attempt to fix issue #5
    elapsed = int(float(info[4].split(",")[0].strip()))

    formatting_args = {
        "status": "Playing" if info[0] == "PLAYING" else "Paused",
        "state": info[0],
        "song": info[1],
        "artist": info[2],
        "album": info[3],
    }

    # Format arguments
    status = {}

    status["large_text"] = statuses["large_text"].format(**formatting_args)
    status["details"] = statuses["details"].format(**formatting_args)
    status["state"] = statuses["state"].format(**formatting_args)

    status["small_image"] = (
        ("play" if info[0] == "PLAYING" else "pause")
        if config.config.get("show_play_pause_icon", True)
        else None
    )
    status["start"] = (time.time() - elapsed) if info[0] == "PLAYING" else None

    return status


def rp_updater():
    """Main Rich Presence loop"""
    statuses = {
        "large_text": config.config.get("large_text")
        or "Using AppleMusicRP (wxllow/applemusicrp) :)",
        "details": config.config.get("details") or "{song}",
        "state": config.config.get("state") or "By {artist} on {album}",
    }

    err_count = 0

    last_played = time.time()

    artwork = "logo"
    current_song = None

    while True:
        try:
            # info[0] is status (PLAYING, PAUSED, or STOPPED), info[1] is title, info[2] is artist, info[3] is album, info[4] is player position
            info = get_music_info()

            if info[0] == "PLAYING" and (time.time()) < (last_played + (10 * 60)):
                if current_song != (info[1], info[2]):
                    artwork = get_cover_art_url(info[1], info[2], info[3]) or "logo"
                    current_song = (info[1], info[2])

                status = get_rp(info, statuses)

                status["large_image"] = artwork

                last_played = time.time()

                RPC.update(**status)
            else:
                RPC.clear()
        except Exception as e:
            log.exception(e)
            err_count += 1

            if err_count < 3:
                msg = "An unexpected error has occured while trying to update your Discord status!"
                dialite.fail("AppleMusicRP", msg)
                time.sleep(1)  # Sleep an extra second

            if err_count > 5:
                dialite.fail("AppleMusicRP", "Too many errors, exiting...")
                exit(1)

        time.sleep(0.8)
