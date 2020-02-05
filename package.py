import PyInstaller.__main__
from os.path import exists
from shutil import copytree, rmtree
from sys import platform

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


color_file_dir = f'{dist_folder}\\color_files'
if exists(color_file_dir): rmtree(color_file_dir)
copytree('colors', color_file_dir)