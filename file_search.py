from pathlib import Path
import os

SEARCH_PATHS = [
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
    Path.home() / "Pictures",
]


def search_file(filename):

    results = []

    for folder in SEARCH_PATHS:

        if not folder.exists():
            continue

        for file in folder.rglob("*"):

            if filename.lower() in file.name.lower():
                results.append(str(file))

    if not results:
        return "File not found."

    return "\n".join(results[:10])


def open_file(filename):

    results = []

    for folder in SEARCH_PATHS:

        if not folder.exists():
            continue

        for file in folder.rglob("*"):

            if filename.lower() in file.name.lower():

                os.startfile(file)

                return f"Opened {file.name}"

    return "File not found."