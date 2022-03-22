import os
import platform
import time
import subprocess
import threading
from sys import exit
import logging
from pypresence import Presence

# Client ID (DO NOT USE FOR ANYTHING OTHER THAN THIS APP PLS!)
client_id = "952320054870020146"
RPC = Presence(client_id)  # Initialize the Presence client

# OS type (Windows, Darwin (macOS), or Linux)
ostype = platform.system()

# Do initial OS-specific stuff
if ostype == 'Darwin':
    import rumps

    macos_ver = platform.mac_ver()[0]

    if int(platform.mac_ver()[0].split('.')[0]) < 10 and int(platform.mac_ver()[0].split('.')[1]) < 15:
        macos_legacy = True
    else:
        macos_legacy = False
elif ostype == 'Windows':
    # Need to find a windows tray library to use and then import it
    pass
else:
    # Needs to be replaced with error dialog
    exit(logging.error("You need to be using Windows or macOS!"))

# Try to connect to RPC
try:
    RPC.connect()
except ConnectionRefusedError:
    # Needs to be replaced with cross-platform error dialog
    exit(rumps.alert("Could not connect to Discord!"))


def get_music_info():
    if ostype == 'Darwin':
        if macos_legacy == True:
            # Legacy script for pre Catalina macOS
            script_loc = os.path.join(os.path.dirname(os.path.realpath(
                __file__)), 'scripts/getmusicinfo-legacy.applescript')
        else:
            # Normal script for macOS
            script_loc = os.path.join(os.path.dirname(os.path.realpath(
                __file__)), 'scripts/getmusicinfo.applescript')

        p = subprocess.Popen(['osascript', script_loc],
                             stdout=subprocess.PIPE)

        out = p.stdout.read().decode("utf-8").strip().split('\\')
    else:
        # Windows support will go here
        pass

    return out


def rp_updater():
    while True:
        # info[0] is status (PLAYING, PAUSED, or STOPPED), info[1] is title, info[2] is artist, info[3] is album
        info = get_music_info()

        if info[0] == "PLAYING" or info[0] == "PAUSED":
            RPC.update(large_image="logo",
                       large_text='Using AppleMusicRP :)',
                       details=f'{"Playing" if info[0] == "PLAYING" else "Paused"} {info[1]}',
                       state=f'By {info[2]} on {info[3]}',
                       start=(
                           (time.time()-int(float(info[4]))) if info[0] == "PLAYING" else None))
        else:
            RPC.clear()

        time.sleep(1)


if ostype == 'Darwin':
    class App(rumps.App):
        pass


if __name__ == '__main__':
    x = threading.Thread(target=rp_updater, daemon=True)
    x.start()

    if ostype == 'Darwin':
        app = App('🎵')
        exit(app.run())
