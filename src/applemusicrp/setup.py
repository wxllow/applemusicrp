"""
This is a setup.py script generated by py2applet

For Windows setup file, see setup-win.py

Usage:
    python setup.py py2app
"""

from setuptools import setup

install_dependencies = ['pypresence',
                        'pystray', 'dialite', 'coverpy', 'appdirs']

APP = ['applemusicrp.py']
DATA_FILES = [('scripts', ['scripts/']), ('assets', ['assets/'])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '3.0.0',
        'LSUIElement': True,
    },
    'packages': install_dependencies
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=install_dependencies
)