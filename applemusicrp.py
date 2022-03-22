import os
import platform
import time
import subprocess
import threading
import rumps
import logging
from pypresence import Presence

client_id = "952320054870020146"  # Put your Client ID in here
RPC = Presence(client_id)  # Initialize the Presence client
reloadable = False

# OS type (Windows, Darwin (macOS), or Linux)
ostype = platform.system()

# Detect if macOS is being used and if so, detect if a macOS version pre-catalina is being used
if ostype == 'Darwin':
    macos_ver = platform.mac_ver()[0]

    if int(platform.mac_ver()[0].split('.')[0]) < 10 and int(platform.mac_ver()[0].split('.')[1]) < 15:
        macos_legacy = True
    else:
        macos_legacy = False
else:
    exit(rumps.alert("You need to be using macOS!"))

try:
    RPC.connect()
except ConnectionRefusedError:
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

        try:
            if info[0] == "PLAYING" or info[0] == "PAUSED":
                RPC.update(large_image="logo",
                           large_text='Using AppleMusicRP :)',
                           details=f'{"Playing" if info[0] == "PLAYING" else "Paused"} {info[1]}',
                           state=f'By {info[2]} on {info[3]}')
            else:
                RPC.clear()
        except Exception as e:
            reloadable = True
            logging.error(e)
            return exit(rumps.alert("Connection to Wumpus has been lost! :(\n AppleMusicRP!"))

        time.sleep(1)


class App(rumps.App):
    pass


if __name__ == '__main__':
    x = threading.Thread(target=rp_updater, daemon=True)
    x.start()
    app = App('🎵')
    app.run()
