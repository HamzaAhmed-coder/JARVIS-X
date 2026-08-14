import os


from pathlib import Path
import os


def get_location(location):

    home = Path.home()

    # OneDrive Desktop
    desktop = home / "OneDrive" / "Desktop"

    # Agar OneDrive na ho
    if not desktop.exists():
        desktop = home / "Desktop"

    documents = home / "OneDrive" / "Documents"
    if not documents.exists():
        documents = home / "Documents"

    pictures = home / "OneDrive" / "Pictures"
    if not pictures.exists():
        pictures = home / "Pictures"

    downloads = home / "Downloads"

    locations = {
        "desktop": str(desktop),
        "documents": str(documents),
        "downloads": str(downloads),
        "pictures": str(pictures),
    }
    return locations.get(location.lower(), os.getcwd())


def create_folder(folder_name, location="project"):

    path = os.path.join(get_location(location), folder_name)

    print(path)

    os.makedirs(path, exist_ok=True)

    return f"Folder '{folder_name}' created in {location}."


def create_text_file(file_name, location="project"):

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    path = os.path.join(get_location(location), file_name)

    with open(path, "w", encoding="utf-8") as f:
        f.write("")

    return f"File '{file_name}' created in {location}."


def delete_file(file_name, location="project"):

    if not file_name.endswith(".txt"):
        file_name += ".txt"

    path = get_location(location)

    file_path = os.path.join(path, file_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        return f"Deleted file '{file_name}'."

    return f"File '{file_name}' not found."


def delete_folder(folder_name, location="project"):

    folder_path = os.path.join(get_location(location), folder_name)

    if os.path.exists(folder_path):
        os.rmdir(folder_path)
        return f"Deleted folder '{folder_name}'."

    return f"Folder '{folder_name}' not found."