from setuptools import setup

APP = ['applemusicrp.py']
DATA_FILES = [('scripts', ['scripts/']), ('assets', ['assets/'])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '1.1.0',
        'LSUIElement': True,
    },
    'packages': ['rumps', 'pypresence', 'infi.systray'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps', 'pypresence']
)
