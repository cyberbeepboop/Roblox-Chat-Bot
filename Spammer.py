import pydirectinput
import pygetwindow
import time
import pyperclip
import syscolors
import random
import pyautogui
from pynput import keyboard as kb

# Global flag for ESC key
running = True

def on_release(key):
    global running
    try:
        if key == kb.Key.esc:
            running = False
            print(f"\n{syscolors.RED}Stopped!{syscolors.RESET}")
            return False
    except AttributeError:
        pass

# Read settings
with open("settings.txt", "r") as f:
    lines = [line for line in f.readlines() if "=" in line]
    messages_raw = lines[0].split("=")[1].strip()
    messages = [msg.strip() for msg in messages_raw.split(",")]
    delay = float(lines[1].split("=")[1].strip())
    window_name = lines[2].split("=")[1].strip().strip('"')
    chat_key = lines[3].split("=")[1].strip().strip('"')
    use_random = lines[4].split("=")[1].strip().lower() == "true"

# Show config
print(f"{syscolors.MAGENTA}{'='*50}")
print(f"{syscolors.BOLD}{syscolors.MAGENTA}  ✦ CONFIGURATION ✦{syscolors.RESET}")
print(f"{syscolors.MAGENTA}{'='*50}")
print(f"{syscolors.BOLD}{syscolors.MAGENTA}Messages{syscolors.RESET}:")
for i, msg in enumerate(messages, 1):
    print(f"  {i}. {syscolors.CYAN}{msg}{syscolors.RESET}")
print(f"{syscolors.BOLD}{syscolors.MAGENTA}Delay{syscolors.RESET}: {syscolors.CYAN}{delay}{syscolors.RESET} seconds")
print(f"{syscolors.BOLD}{syscolors.MAGENTA}Window{syscolors.RESET}:  {syscolors.CYAN}{window_name}{syscolors.RESET}")
print(f"{syscolors.BOLD}{syscolors.MAGENTA}Chat Key{syscolors.RESET}: {syscolors.CYAN}{chat_key}{syscolors.RESET}")
print(f"{syscolors.BOLD}{syscolors.MAGENTA}Random Mode{syscolors.RESET}: {syscolors.CYAN}{'ON' if use_random else 'OFF'}{syscolors.RESET}")
print(f"{syscolors.MAGENTA}{'='*50}{syscolors.RESET}\n")

# Wait for user
print(f"{syscolors.GREEN}Make sure the game window is open and ready!{syscolors.RESET}")
print(f"{syscolors.YELLOW}Starting in 5 seconds... Press ESC to stop.{syscolors.RESET}\n")
time.sleep(5)

# Get window and activate
try:
    window = pygetwindow.getWindowsWithTitle(window_name)[0]
    window.activate()
    time.sleep(0.5)
except:
    print(f"{syscolors.RED}Could not find window: {window_name}{syscolors.RESET}")
    exit()

# Start listener for ESC key
listener = kb.Listener(on_release=on_release)
listener.start()

# Start spamming
try:
    print(f"{syscolors.GREEN}Spamming started!{syscolors.RESET}\n")
    while running:
        # Pick message
        if use_random:
            message = random.choice(messages)
        else:
            message = messages[0]
        
        # Open chat
        pydirectinput.press(chat_key)
        time.sleep(0.3)
        
        # Paste message
        pyperclip.copy(message)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.1)
        
        # Send
        pydirectinput.press("enter")
        time.sleep(delay)
        
except KeyboardInterrupt:
    print(f"\n{syscolors.RED}Stopped!{syscolors.RESET}")
finally:
    listener.stop()