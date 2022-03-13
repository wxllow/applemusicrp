import os
import time
import subprocess
import threading
import rumps
from pypresence import Presence

client_id = "952320054870020146"  # Put your Client ID in here
RPC = Presence(client_id)  # Initialize the Presence client
reloadable = False

try:
    RPC.connect()
except ConnectionRefusedError:
    exit(rumps.alert("Could not connect to Discord!"))


def get_music_info():
    p = subprocess.Popen(['osascript', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts/getmusicinfo.applescript')],
                         stdout=subprocess.PIPE)

    out = p.stdout.read().decode("utf-8").strip().split('\\')

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
        except:
            reloadable = True
            return exit(rumps.alert("Connection to Wumpus has been lost! :(\n AppleMusicRP!"))

        time.sleep(1)


class App(rumps.App):
    pass


if __name__ == '__main__':
    x = threading.Thread(target=rp_updater, daemon=True)
    x.start()
    app = App('🎵')
    app.run()
