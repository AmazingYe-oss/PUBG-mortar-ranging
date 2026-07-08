import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'pubg_distance.py',
    '--name=PUBG距离测量工具',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--add-data=config.json;.' if os.path.exists('config.json') else '',
    '--clean',
    '--noconfirm'
])
