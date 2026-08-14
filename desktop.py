import os
import subprocess


def open_desktop():
    path = os.path.join(os.path.expanduser("~"), "Desktop")
    subprocess.Popen(["explorer.exe", path])
    return "Opening Desktop"


def open_downloads():
    path = os.path.join(os.path.expanduser("~"), "Downloads")
    subprocess.Popen(["explorer.exe", path])
    return "Opening Downloads"

def open_documents():
    path = os.path.join(os.path.expanduser("~"), "Documents")
    subprocess.Popen(["explorer.exe", path])
    return "Opening Documents"


def open_pictures():
    path = os.path.join(os.path.expanduser("~"), "Pictures")
    subprocess.Popen(["explorer.exe", path])
    return "Opening Pictures"


def open_file_explorer():
    subprocess.Popen("explorer")
    return "Opening File Explorer"


def open_cmd():
    subprocess.Popen("cmd")
    return "Opening Command Prompt"


def open_paint():
    subprocess.Popen("mspaint")
    return "Opening Paint"


def open_vscode():
    subprocess.Popen("code")
    return "Opening VS Code"