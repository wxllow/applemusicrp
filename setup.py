from setuptools import setup
import platform

# py2app
APP = ['applemusicrp.py']
DATA_FILES = [('scripts', ['scripts/']), ('assets', ['assets/'])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '2.0.0',
        'LSUIElement': True,
    },
    'packages': ['rumps', 'pypresence'],
}

install_dependencies = ['pypresence', 'rumps']

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'setuptools'],
    install_requires=install_dependencies
)
