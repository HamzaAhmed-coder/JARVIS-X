import pyperclip


def copy_text(text):

    pyperclip.copy(text)

    return f"Copied: {text}"


def read_clipboard():

    text = pyperclip.paste()

    if not text:
        return "Clipboard is empty."

    return text