from setuptools import setup
import platform

# py2app
APP = ['applemusicrp.py']
DATA_FILES = [('scripts', ['scripts/']), ('assets', ['assets/'])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '1.1.0',
        'LSUIElement': True,
    },
    'packages': ['rumps', 'pypresence'],
}

install_dependencies = ['pypresence']

if platform.system() == 'Darwin':
    install_dependencies.append('rumps')
elif platform.system() == 'Windows':
    install_dependencies.append('pywin32')
    install_dependencies.append('infi.systray')
    install_dependencies.append('psutil')

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=install_dependencies
)
