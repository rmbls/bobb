from setuptools import setup

APP = ['Lagence Project.py']
OPTIONS = {
    'argv_emulation': True,
    'packages': [],
    'excludes': ['PyInstaller', 'PySide2', 'PySide6', 'packaging', 'backports', 'backports.tarfile']
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['jaraco.text'],
)