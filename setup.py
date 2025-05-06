from setuptools import setup, Command
import subprocess

class PyInstallerCommand(Command):
    description = "Build the project using PyInstaller"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.check_call([
            'pyinstaller',
            '--onefile',
            '--windowed',
            'Lagence Project.py'
        ])

setup(
    name='LagenceProject',
    version='1.0',
    description='A script to transform Lagence spreadsheets into a format that can be imported into Catsy. Requires Python with Tkinter support.',
    author='Darek from Catsy',
    packages=[],
    install_requires=[
        'jaraco.text', 'numpy', 'pandas', 'openpyxl', 'xlrd'
    ],
    cmdclass={
        'pyinstaller': PyInstallerCommand,
    },
)