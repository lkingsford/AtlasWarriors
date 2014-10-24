import sys
import re
import version
from cx_Freeze import setup, Executable

# Makes exe with command "python setup.py build_exe" 

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"], 'include_msvcr':True,
"include_files": ["DejaVuSans.ttf", "DejaVuSansMono.ttf", "DejaVuSerif.ttf", "items.xml"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
#Should uncomment next lines to get rid of console
#if sys.platform == "win32":
    #base = "Win32GUI"

setup(  name = "Atlas Warriors",
        version = version.Version(),
        description = "Roguelike Game",
        options = {"build_exe": build_exe_options},
        executables = [Executable("rl.py", base=base)])


