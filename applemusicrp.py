import sys
import os
import platform
import time
import subprocess
import threading
from sys import exit
import logging
from pypresence import Presence
import dialite

# Lazy fix for py2exe
try:
    __file__
except NameError:
    __file__ = sys.argv[0]


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
    from infi.systray import SysTrayIcon
    import win32com.client
    import pythoncom
    import psutil

    systray = SysTrayIcon(os.path.join(os.path.dirname(os.path.realpath(
        __file__)), 'assets/icon.ico'), "AppleMusicRP", ())
else:
    dialite.fail("AppleMusicRP", "You need to be using Windows or macOS!")
    exit(1)

# Try to connect to RPC
try:
    RPC.connect()
except ConnectionRefusedError:
    # Needs to be replaced with cross-platform error dialog
    dialite.fail("AppleMusicRP", "Could not connect to Discord!")
    exit(1)


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

        return p.stdout.read().decode("utf-8").strip().split('\\')
    else:
        if "iTunes.exe" in (p.name() for p in psutil.process_iter()):
            itunes = win32com.client.Dispatch(
                "iTunes.Application", pythoncom.CoInitialize())
        else:
            return ['STOPPED']

        current_track = itunes.CurrentTrack
        playerstate = itunes.PlayerState

        if current_track is None:
            return ['STOPPED']

        return [('PAUSED' if playerstate == 0 else 'PLAYING'), current_track.Name, current_track.Artist,
                current_track.Album, str(itunes.PlayerPosition)]  # Test


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
    else:
        exit(systray.start())
