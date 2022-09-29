import logging
import os
import platform
import subprocess
import sys
import threading
import time
from sys import exit

import dialite
import pypresence.exceptions
from pypresence import Presence
from rich.logging import RichHandler

from .config import Config
from .utils import get_cover_art_url

# Lazy fix for py2exe
try:
    __file__
except NameError:
    __file__ = sys.argv[0]

# Logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(message)s",
    handlers=[RichHandler()],
)

log = logging.getLogger("rich")

# Load configuration
config = Config()

# Initiate RPC
client_id = config.config.get("client_id", "952320054870020146")  # Client ID
RPC = Presence(client_id)  # Initialize the Presence clie

# Possible values: "Darwin", "Windows", "Linux"
ostype = platform.system()

log.warning(__file__)

# Do initial OS-specific stuff
if ostype == "Darwin":
    import rumps

    macos_ver = platform.mac_ver()[0]

    macos_legacy = bool(
        int(platform.mac_ver()[0].split(".")[0]) < 10
        and int(platform.mac_ver()[0].split(".")[1]) < 15
    )
elif ostype == "Windows":
    import pythoncom
    import win32com.client
    from PIL import Image
    from pystray import Icon, Menu, MenuItem
else:
    # There isn't iTunes for Linux :(
    dialite.fail("AppleMusicRP", "You need to be using Windows or macOS!")
    exit(1)

# Try to connect to RPC
try:
    RPC.connect()
except (
    ConnectionRefusedError,
    pypresence.exceptions.DiscordNotFound,
    pypresence.exceptions.DiscordError,
) as e:
    log.exception(e)
    dialite.fail("AppleMusicRP", "Could not connect to Discord!")
    exit(1)


def get_music_info():
    if ostype == "Darwin":
        # Get info using AppleScript and then parse
        if macos_legacy:
            # Legacy script for pre-catalina macOS
            script_loc = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "scripts/getmusicinfo-legacy.applescript",
            )
        else:
            # Normal script for macOS
            script_loc = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "scripts/getmusicinfo.applescript",
            )

        p = subprocess.Popen(["osascript", script_loc], stdout=subprocess.PIPE)

        return p.stdout.read().decode("utf-8").strip().split("\\")
    else:
        # # Check for running iTunes
        # try:
        #     win32com.client.GetActiveObject("Itunes.Application")
        # except:
        #     return ["STOPPED"]

        # Check if iTunes is running
        itunes = win32com.client.Dispatch(
            "iTunes.Application", pythoncom.CoInitialize()
        )

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

            if (
                info[0] == "PLAYING"
                or info[0] == "PAUSED"
                and (time.time()) < (last_played + (10 * 60))
            ):
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
                exit(0)

        time.sleep(0.8)


"""Menu bar/tray"""


def toggle_playpause_icon():
    config.config["show_play_pause_icon"] = config.config.get("show_play_pause_icon")

    config.save()


def main():
    # Launch Rich Presence (RP) updating thread
    x = threading.Thread(target=rp_updater, daemon=True)
    x.start()

    # Start menu bar app
    if ostype == "Windows":

        def quit():
            tray.stop()
            exit(0)

        menu = Menu(
            MenuItem(
                "Toggle play/pause icon",
                toggle_playpause_icon,
                checked=lambda item: config.config.get("show_play_pause_icon", True),
            ),
            MenuItem("Quit", quit),
        )

        image = Image.open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets/icon.png")
        )

        tray = Icon("AppleMusicRP", image, "AppleMusicRP", menu=menu)

        tray.run()
    else:

        class DarwinStatusBar(rumps.App):
            def __init__(self):
                super(DarwinStatusBar, self).__init__("AppleMusicRP")
                toggle = rumps.MenuItem("Toggle play/pause icon")
                toggle.state = (
                    1 if config.config.get("show_play_pause_icon", True) else 0
                )
                self.menu = [toggle]

            @rumps.clicked("Toggle play/pause icon")
            def onoff(self, sender):
                toggle_playpause_icon()
                sender.state = config.config["show_play_pause_icon"]

        DarwinStatusBar().run()


if __name__ == "__main__":
    main()
