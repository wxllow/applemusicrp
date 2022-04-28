import sys
import os
import platform
import time
import subprocess
import threading
from sys import exit
import logging
from pypresence import Presence
import pypresence.exceptions
import dialite
from pystray import Icon as icon, Menu as menu, MenuItem as item
from PIL import Image
from utils import get_cover_art_url
from config import Config


# Lazy fix for py2exe
try:
    __file__
except NameError:
    __file__ = sys.argv[0]

# Client ID (DO NOT USE FOR ANYTHING OTHER THAN THIS APP PLS!)
client_id = "952320054870020146"
RPC = Presence(client_id)  # Initialize the Presence client
config = Config()

ostype = platform.system()

# Do initial OS-specific stuff
if ostype == 'Darwin':
    macos_ver = platform.mac_ver()[0]

    macos_legacy = bool(int(platform.mac_ver()[0].split('.')[0]) < 10 and int(
        platform.mac_ver()[0].split('.')[1]) < 15)
elif ostype == 'Windows':
    # Windows needs a lot of dependencies :p
    import win32com.client
    import pythoncom
    import psutil
else:
    # There isn't iTunes for Linux :(
    dialite.fail("AppleMusicRP", "You need to be using Windows or macOS!")
    exit(1)

# Try to connect to RPC
try:
    RPC.connect()
except (ConnectionRefusedError, pypresence.exceptions.DiscordNotFound, pypresence.exceptions.DiscordError) as e:
    msg = 'Could not connect to Discord!'
    dialite.fail("AppleMusicRP", msg)
    logging.exception(msg)
    exit(1)


def get_music_info():
    if ostype == 'Darwin':
        # Get info using AppleScript and then parse
        if macos_legacy:
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
        # Check if iTunes is running
        if not "iTunes.exe" in (p.name() for p in psutil.process_iter()):
            return ['STOPPED']

        itunes = win32com.client.Dispatch(
            "iTunes.Application", pythoncom.CoInitialize())

        # Get info using Windows API
        current_track = itunes.CurrentTrack
        playerstate = itunes.PlayerState

        if not current_track:
            return ['STOPPED']

        return [('PAUSED' if playerstate == 0 else 'PLAYING'), current_track.Name, current_track.Artist,
                current_track.Album, str(itunes.PlayerPosition)]


def get_rp(info):
    status = {}

    # .split(',')[0] is an attempt to fix issue #5
    elapsed = int(float(info[4].split(',')[0].strip()))

    status = {
        'large_text': 'Using AppleMusicRP (https://github.com/wxllow/applemusicrp) :)',
        'details': f'{"Playing" if info[0] == "PLAYING" else "Paused"} {info[1]}',
        'small_image': (('play' if info[0] == "PLAYING" else 'pause') if config.config.get(
            'show_play_pause_icon', True) else None),
        'small_text': ('Playing' if info[0] == "PLAYING" else 'Paused'),
        'state': f'By {info[2]} on {info[3]}',
        'start': (
            (time.time()-elapsed) if info[0] == "PLAYING" else None)
    }

    return status


def rp_updater():
    err_count = 0

    last_played = time.time()

    artwork = 'logo'
    current_song = None

    while True:
        try:
            # info[0] is status (PLAYING, PAUSED, or STOPPED), info[1] is title, info[2] is artist, info[3] is album, info[4] is player position
            info = get_music_info()

            if info[0] == "PLAYING" or info[0] == "PAUSED" and (time.time()) < (last_played+(10*60)):
                if current_song != (info[1], info[2]):
                    artwork = get_cover_art_url(
                        info[1], info[2], info[3]) or 'logo'
                    current_song = (info[1], info[2])

                status = get_rp(info)

                status['large_image'] = artwork

                last_played = time.time()

                RPC.update(**status)
            else:
                RPC.clear()
        except:
            err_count += 1

            if err_count < 3:
                msg = 'An unexpected error has occured while trying to update your Discord status!'
                dialite.fail("AppleMusicRP", msg)
                logging.exception(msg)
                time.sleep(1)  # Sleep an extra second

            if err_count > 5:
                logging.exception(msg)
                exit(0)

        time.sleep(0.8)


"""Menu bar/tray"""


def quit():
    tray.stop()
    exit(0)


def toggle_playpause_icon():
    if config.config.get('show_play_pause_icon', True):
        config.config['show_play_pause_icon'] = False
    else:
        config.config['show_play_pause_icon'] = True

    config.save()


image = Image.open(os.path.join(os.path.dirname(os.path.realpath(
    __file__)), 'assets/icon.png'))


menu = menu(item('Toggle play/pause icon', toggle_playpause_icon,
            checked=lambda item: config.config.get('show_play_pause_icon', True)), item('Quit', quit))

tray = icon('AppleMusicRP', image, 'AppleMusicRP', menu=menu)


if __name__ == '__main__':
    # Launch Rich Presence (RP) updating thread
    x = threading.Thread(target=rp_updater, daemon=True)
    x.start()

    # Start menu bar app
    tray.run()
