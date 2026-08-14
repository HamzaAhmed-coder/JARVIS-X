import os
import subprocess
import pyautogui


def take_screenshot():

    image = pyautogui.screenshot()

    image.save("screenshot.png")

    return "Screenshot saved."


def lock_pc():

    subprocess.run(
        "rundll32.exe user32.dll,LockWorkStation"
    )

    return "Computer Locked."


def shutdown_pc():

    os.system("shutdown /s /t 5")

    return "Computer will shutdown in 5 seconds."


def restart_pc():

    os.system("shutdown /r /t 5")

    return "Computer will restart in 5 seconds."


def sleep_pc():

    os.system(
        "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
    )

    return "Computer Sleeping."