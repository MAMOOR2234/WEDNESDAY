#live ai can control my screen and other aspects of my computer and do what i have told him to do
 #include the necessary imports and functionality
import pyautogui 
import time 

pyautogui.FAIL_SAFE = True
pyautogui.PAUSE = 0.5

def run_command(command: str):
 command = command.lower().strip()

    if "open start menu" in command:
        pyautogui.press("win")

    elif "close window" in command:
        pyautogui.hotkey("alt", "f4")

    elif "copy" in command:
        pyautogui.hotkey("ctrl", "c")

    elif "paste" in command:
        pyautogui.hotkey("ctrl", "v")

    elif command.startswith("type "):
        text = command.replace("type ", "", 1)
        pyautogui.write(text, interval=0.03)

    elif "press enter" in command:
        pyautogui.press("enter")

    elif "take screenshot" in command:
        filename = f"screenshot_{int(time.time())}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print("Saved:", filename)

    elif command.startswith("click "):
        # example: click 500 300
        parts = command.split()
        x = int(parts[1])
        y = int(parts[2])
        pyautogui.click(x, y)

    elif command.startswith("move mouse "):
        # example: move mouse 400 200
        parts = command.split()
        x = int(parts[2])
        y = int(parts[3])
        pyautogui.moveTo(x, y, duration=0.3)

    else:
        print("Unknown command:", command)

if __name__ == "__main__":
    while True:
        user_input = input("AI command: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        run_command(user_input)
