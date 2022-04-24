# AppleMusicRP - Apple Music Discord Rich Presence

A simple and light-weight menu bar application providing Discord Rich Presence support for Apple Music/iTunes on macOS and Windows, **now with album art**!

## Highlights

- Light-weight
- Easy to use, all you need to do is run the app, no configuration required!
- Fetches and displays album artwork
- Shows time elapsed (How far into the song you are)
- Status disappears after music is paused for >10 minutes and when no music is playing
- Universal Application (on macOS)

## Screenshots

### Screenshot while playing

![Screenshot while playing](screenshots/screenshot1.png)

### Screenshot while paused

![Screenshot while paused](screenshots/screenshot2.png)

## Usage

### macOS

#### Homebrew
 
If you have homebrew installed, use this command to install AppleMusicRP:

`brew install wxllow/based/applemusicrp`

#### Manually

- Download the latest version (in Releases), double click it, and move the .app "file" to your Applications folder (or wherever you wish.)
- Run it (Make sure Discord is running; If you get an "Unidentified Developer" error, alt+click the application and then click Open.)
- That's it! You should now see a 🎵 icon in your menu bar :)!

### Windows

- Download the latest version (in Releases) and run the installer (or extract the portable version)! 
- Run the application, which will be located either in `C:\Program Files\AppleMusicRP` or wherever u extracted the portable version. (Make sure Discord is running)
- That's it! You should now see a 🎵 icon in your system tray :)!

## Building
### macOS

**If you want to build a universal application, make sure you are using [Python 3.9.x universal2 from Python's website](https://www.python.org/downloads/macos/) and not the homebrew version.**

`brew install create-dmg`

`python3 -m pip install wheel py2app pystray pillow pypresence dialite coverpy appdirs toml`

`chmod +x ./build.zsh; ./build.zsh`

### Windows

`pip install wheel py2exe pypresence pyinstaller pywin32 psutil pystray pillow dialite coverpy appdirs toml`

`.\build.bat`
  
## Credits

- [Material Icons](https://fonts.google.com/icons)
- [Coverpy](https://github.com/matteing/coverpy)
- [Pypresence](https://qwertyquerty.github.io/pypresence/html/index.html)

## Notice

iTunes, Apple, and Apple Music are registered trademarks of Apple Inc.
Discord is a registered trademark of Discord Inc.

This application is unofficial and was made for fun, it is not endorsed by Apple nor Discord.
