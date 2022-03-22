from setuptools import setup

APP = ['applemusicrp.py']
DATA_FILES = [('scripts', ['scripts/'])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,
    },
    'packages': ['rumps', 'pypresence'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'], install_requires=['rumps', 'pypresence']
)
