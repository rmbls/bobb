from setuptools import setup

APP = ['Lagence Project.py']
OPTIONS = {
    'argv_emulation': True,
    'includes': ['numpy', 'pandas', 'jaraco.text'],
    'excludes': [
        'PyInstaller', 'PySide2', 'PySide6', 'packaging', 'backports', 'backports.tarfile',
        'tkinter', '_tkinter'
    ]
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    install_requires=['jaraco.text', 'numpy', 'pandas'],
)