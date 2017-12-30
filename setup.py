import sys
from cx_Freeze import setup, Executable

setup(
    name ='Bomber ',
    author='Marishwaran',
    version = '1.0',
    options={'build_exe':{'include_files':['bomb.png','wall.png','mob.png','flame.png','bicon.png','bback.png','bfront.png','bright.png','bwall.png','map1.txt','map2.txt','highscore.txt']}},
    executables = [Executable('bomb.py', base = 'Win32GUI')])
