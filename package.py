import sys
import PyInstaller.__main__

is_windows = sys.platform == 'win32'
sep = ';' if is_windows else ':' # Platform specific data separator

PyInstaller.__main__.run([
    '--name=Color Identifier',
    '--onefile',
    '--windowed',
    f'--add-data=icon\\*.png{sep}icon',
    f'--add-data=colors.txt{sep}.',
    f'--add-data=colors-shades.txt{sep}.',
    '--icon=icon\\icon.ico',
    '--distpath=dist',
    'main.py',
])