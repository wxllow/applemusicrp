import asyncio
import os
import platform
import threading
from sys import exit

import dialite
import pypresence.exceptions

from .config import Config
from .rpc import connect, rp_updater
from .utils import ostype, path

# Load configuration
config = Config()

# Do initial OS-specific stuff
if ostype == "Darwin":
    import rumps

    macos_ver = platform.mac_ver()[0]

    macos_legacy = bool(
        int(platform.mac_ver()[0].split(".")[0]) < 10
        and int(platform.mac_ver()[0].split(".")[1]) < 15
    )
elif ostype == "Windows":
    from PIL import Image
    from pystray import Icon, Menu, MenuItem
else:
    # There isn't iTunes for Linux :(
    dialite.fail(
        "AppleMusicRP", "You need to be using Windows or macOS, not {ostype!r}!"
    )
    exit(1)


"""Menu bar/tray"""


def toggle_playpause_icon() -> None:
    config.config["show_play_pause_icon"] = not config.config.get(
        "show_play_pause_icon", True
    )
    config.save()


def try_connect() -> bool:
    try:
        connect()
        return True
    except (
        ConnectionRefusedError,
        pypresence.exceptions.DiscordNotFound,
        pypresence.exceptions.DiscordError,
    ):
        return False


def rp_thread() -> None:
    """Rich Presence thread function"""
    try:
        asyncio.get_event_loop()
    except:
        asyncio.set_event_loop(asyncio.new_event_loop())

    while True:
        # Try connecting until successful
        while True:
            if try_connect():
                break

        rp_updater()


def main() -> None:
    connected = False

    # Launch Rich Presence (RP) updating thread
    x = threading.Thread(target=rp_thread, daemon=True)
    x.start()

    # Start menu bar app
    if ostype == "Darwin":

        class DarwinStatusBar(rumps.App):
            def __init__(self):
                super(DarwinStatusBar, self).__init__("AppleMusicRP")
                toggle = rumps.MenuItem("Toggle play/pause icon")
                toggle.state = (
                    1 if config.config.get("show_play_pause_icon", True) else 0
                )
                self.menu = [
                    toggle,
                ]

            @rumps.clicked("Toggle play/pause icon")
            def onoff(self, sender):
                toggle_playpause_icon()
                sender.state = config.config["show_play_pause_icon"]

        DarwinStatusBar().run()
    else:

        def quit():
            tray.stop()

        menu = Menu(
            MenuItem(
                "Toggle play/pause icon",
                toggle_playpause_icon,
                checked=lambda item: config.config.get("show_play_pause_icon", True),
            ),
            MenuItem("Quit", quit),
        )

        image = Image.open(os.path.join(path, "assets", "icon.png"))

        tray = Icon("AppleMusicRP", image, "AppleMusicRP", menu=menu)

        tray.run()


if __name__ == "__main__":
    main()
