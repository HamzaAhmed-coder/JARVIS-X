import subprocess
import subprocess
import shutil
import os

import subprocess
import shutil
import os


# =========================================
# BASIC WINDOWS APPS
# =========================================

def open_calculator():
    print("🔥 INSIDE open_calculator() 🔥")
    subprocess.Popen("calc.exe")
    return "Calculator opened."


def open_notepad():
    print("🔥 INSIDE open_notepad() 🔥")
    subprocess.Popen("notepad.exe")
    return "Notepad opened."


# =========================================
# APPLICATION COMMANDS
# =========================================

APP_COMMANDS = {

    "calculator": "calc.exe",

    "notepad": "notepad.exe",

    "paint": "mspaint.exe",

    "cmd": "cmd.exe",

    "explorer": "explorer.exe",

    "vscode": "code",

    "chrome": "chrome",

}


# =========================================
# OPEN APPLICATION
# =========================================

def open_application(app_name):

    app_name = app_name.lower().strip()

    command = APP_COMMANDS.get(app_name)

    if not command:

        return (
            f"I don't know how to open "
            f"'{app_name}'."
        )

    try:

        subprocess.Popen(
            command,
            shell=True
        )

        return (
            f"Opening {app_name}..."
        )

    except Exception as e:

        return (
            f"Unable to open "
            f"{app_name}: {e}"
        )


# =========================================
# WINDOWS FOLDERS
# =========================================

FOLDER_PATHS = {

    "desktop":
        os.path.join(
            os.path.expanduser("~"),
            "Desktop"
        ),

    "downloads":
        os.path.join(
            os.path.expanduser("~"),
            "Downloads"
        ),

    "documents":
        os.path.join(
            os.path.expanduser("~"),
            "Documents"
        ),

    "pictures":
        os.path.join(
            os.path.expanduser("~"),
            "Pictures"
        ),

    "videos":
        os.path.join(
            os.path.expanduser("~"),
            "Videos"
        ),

}


# =========================================
# OPEN FOLDER
# =========================================

def open_folder(folder_name):

    folder_name = (
        folder_name
        .lower()
        .strip()
    )

    path = FOLDER_PATHS.get(
        folder_name
    )

    if not path:

        return (
            f"I don't know the "
            f"'{folder_name}' folder."
        )

    if not os.path.exists(path):

        return (
            f"The {folder_name} "
            f"folder does not exist."
        )

    try:

        os.startfile(path)

        return (
            f"Opening {folder_name}..."
        )

    except Exception as e:

        return (
            f"Unable to open "
            f"{folder_name}: {e}"
        )


# =========================================
# CREATE FOLDER
# =========================================

def create_folder(folder_name):

    folder_name = (
        folder_name
        .strip()
    )

    if not folder_name:

        return "Please provide a folder name."

    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    folder_path = os.path.join(
        desktop,
        folder_name
    )

    try:

        os.makedirs(
            folder_path,
            exist_ok=True
        )

        return (
            f"Folder '{folder_name}' "
            f"created on the Desktop."
        )

    except Exception as e:

        return (
            f"Unable to create folder: {e}"
        )
        
def open_calculator():
    print("🔥 INSIDE open_calculator() 🔥")
    subprocess.Popen("calc.exe")
    return "Calculator opened."

def open_notepad():
    print("🔥 INSIDE open_notepad() 🔥")
    subprocess.Popen("notepad.exe")
    return "Notepad opened."

APP_COMMANDS = {
    "calculator": "calc.exe",
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "explorer": "explorer.exe",
    "vscode": "code",
    "chrome": "chrome",
}


def open_application(app_name):

    app_name = app_name.lower().strip()

    command = APP_COMMANDS.get(app_name)

    if not command:
        return f"I don't know how to open '{app_name}'."

    if shutil.which(command) or command.endswith(".exe"):
        try:
            subprocess.Popen(command)
            return f"Opening {app_name}..."
        except Exception as e:
            return str(e)

    return f"{app_name} is not installed."