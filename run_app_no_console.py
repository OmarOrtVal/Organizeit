import subprocess
import sys
import os

if sys.platform == "win32":
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = 0  
    
    subprocess.Popen(
        [sys.executable.replace("python.exe", "pythonw.exe"), "app.py"],
        creationflags=subprocess.CREATE_NO_WINDOW,
        startupinfo=startupinfo,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
