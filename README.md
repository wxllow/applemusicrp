# AppleMusicRP - Apple Music Discord Rich Presence

**NOTE: There is support for macOS versions before Catalina in 1.1.0 however it is not tested as I do not have access to an Intel Mac...**

A simple and light-weight menu bar application providing Discord Rich Presence support for Apple Music/iTunes! (Currently only for macOS *but Windows support is almost here*!)

## Highlights

- Light-weight (Uses only 0.5% CPU and less than 40MB of memory on 2020 M1 Macbook Air)
- Easy to install/use, all you need to do is run the app, no configuration required!
- Universal Application (on macOS)
- Shows time elapsed (How far into the song you are)

## Usage

### Windows (Coming soon)

- Download the latest version (in Releases) and run the exe file!
- That's it! You should now see a 🎵 icon in your system tray :)!

### macOS

- Download the latest version (in Releases), double click it, and move the .app "file" to your Applications folder (or wherever you wish.)
- Run it (If you get an "Unidentified Developer" error, alt+click the application and then click Open.)
- That's it! You should now see a 🎵 icon in your menu bar :)!

## Building

### Windows

***Not complete yet...***

`pip install py2exe pywin32 infi.systray`

### macOS

`python3 -m pip install py2app rumps pypresence`
`python3 setup.py py2app`

## Planned Features

- ~~Time elapsed~~ **DONE!**
- ~~Support for pre-10.15 macOS (Should be a simple change of `tell application "Music"` to `tell application "iTunes")~~ **DONE!**
- Windows support [**ALMOST DONE!!**](https://github.com/wxllow/applemusicrp/milestone/1)
- Anything else that is suggested and reasonable :)

## Acknowledgments

- [Rumps - Ridiculously Uncomplicated macOS Python Statusbar apps](https://github.com/jaredks/rumps)
- [pypresence](https://github.com/qwertyquerty/pypresence)
- [py2app](https://github.com/ronaldoussoren/py2app/)

## References

- [pypresence docs](https://qwertyquerty.github.io/pypresence/html/index.html)
- [Create a macOS Menu Bar App with Python](https://camillovisini.com/article/create-macos-menu-bar-app-pomodoro/#project-setup)
- <https://apple.stackexchange.com/questions/406941/applescript-and-music>

## Notice

iTunes, Apple, and Apple Music are registered trademarks of Apple Inc.
Discord is a registered trademark of Discord Inc.

This application is unofficial and was made for fun, it is not endorsed by Apple nor Discord.
