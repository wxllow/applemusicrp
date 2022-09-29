<div align="center">

# AppleMusicRP - Discord Rich Presence for Apple Music

![Downloads](https://img.shields.io/github/downloads/wxllow/applemusicrp/total) ![GitHub release (latest by SemVer)](https://img.shields.io/github/downloads/wxllow/applemusicrp/latest/total) ![GitHub forks](https://img.shields.io/github/forks/wxllow/applemusicrp) ![GitHub stars](https://img.shields.io/github/stars/wxllow/applemusicrp)  ![GitHub contributors](https://img.shields.io/github/contributors/wxllow/applemusicrp) ![License](https://img.shields.io/github/license/wxllow/applemusicrp) [![Lint](https://github.com/wxllow/applemusicrp/actions/workflows/black.yml/badge.svg)](https://github.com/wxllow/applemusicrp/actions/workflows/black.yml)

A simple and light-weight menu bar application providing Discord Rich Presence support for Apple Music/iTunes on macOS and Windows, **now with album art**!

![Screenshot](screenshots/screenshot.png)

</div>

## Highlights

- Easy to use
- Fetches and displays album artwork from iTunes (This even works for local songs, as long as they're on iTunes and have the right metadata)
- Shows time elapsed (How far into the song you are)
- Status disappears after music is paused for >10 minutes and when no music is playing
- [Configurable/Customizable](https://github.com/wxllow/applemusicrp/wiki/Configuration)
- Universal Application (on macOS)

## Download

### macOS

If you have homebrew installed, you can use this command to install AppleMusicRP:

`brew install --no-quarantine wxllow/based/applemusicrp`

Otherwise, you can just download the latest DMG from the [releases](https://github.com/wxllow/applemusicrp/releases) tab

### Windows

The latest version is available from the [releases](https://github.com/wxllow/applemusicrp/releases) tab

## Usage

Make sure Discord is running and open the app!

***If you get an "Unidentified Developer" error, option+click the application and then click Open***

## Building

***macOS: If you want to build a universal application, make sure you are using [Python 3 universal2 from Python's website](https://www.python.org/downloads/macos/) and not the homebrew version of Python!***

***Windows: Make sure you're using Python from the Python website and not from the Microsoft Store!***

`poetry install` (If you don't have poetry, install it using `pip install poetry`)

### macOS

`poetry run briefcase build`

`poetry run briefcase package --adhoc-sign`

Outputs to: `macOS`

### Windows

`poetry run python setup_win.py py2exe`

Outputs to: `dist\windows`

## Notes (for devs)

- AppleMusicRP uses two libraries for the system tray: pystray for Windows and rumps for macOS. Even though pystray is cross-platform, using it led to issues with compatibility and universal apps (see https://github.com/wxllow/applemusicrp/issues/21 and https://github.com/wxllow/applemusicrp/issues/20)

## Credits

- [Material Icons](https://fonts.google.com/icons)
- [Coverpy](https://github.com/matteing/coverpy)
- [Pypresence](https://qwertyquerty.github.io/pypresence/html/index.html)
- [Everyone who has made issues/pull requests or has suggested improvements](https://github.com/wxllow/applemusicrp/issues?q=)
- [And to all the dependencies that make this possible!](https://github.com/wxllow/applemusicrp/network/dependencies)

## License

The code of this project itself is licensed under the [MIT license](LICENSE). The logo and play/pause icons are licensed under the [Apache License 2.0](https://github.com/google/material-design-icons/blob/master/LICENSE). Dependencies used in this project have their respective licenses.

## Notice

iTunes, Apple, and Apple Music are registered trademarks of Apple Inc.
Discord is a registered trademark of Discord Inc.

This application is unofficial and was made for fun, it is not endorsed by Apple nor Discord.
