from sys import platform
from shutil import copytree
import PyInstaller.__main__

is_windows = platform == 'win32'
sep = ';' if is_windows else ':' # Platform specific data separator

dist_folder = 'dist'

PyInstaller.__main__.run([
    '--name=Color Identifier',
    '--onefile',
    '--windowed',
    f'--add-data=icon\\*.png{sep}icon',
    f'--add-data=colors.txt{sep}.',
    '--icon=icon\\icon.ico',
    f'--distpath={dist_folder}',
    'main.py',
])

copytree('colors', f'{dist_folder}\\color_files')