import webbrowser
from urllib.parse import quote


def open_url(url):
    webbrowser.open(url)
    return f"Opened {url}"


def google_search(query):
    url = f"https://www.google.com/search?q={quote(query)}"
    webbrowser.open(url)
    return f"Searching Google for: {query}"


def youtube_search(query):
    url = f"https://www.youtube.com/results?search_query={quote(query)}"
    webbrowser.open(url)
    return f"Searching YouTube for: {query}"

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube"

def open_instagram():
    webbrowser.open("https://www.instagram.com")
    return "Opening Instagram"

def open_chatgpt():
    webbrowser.open("https://chatgpt.com")
    return "Opening ChatGPT"


def open_linkedin():
    webbrowser.open("https://www.linkedin.com")
    return "Opening LinkedIn"


def open_github():
    webbrowser.open("https://github.com")
    return "Opening GitHub"


def open_google():
    webbrowser.open("https://www.google.com")
    return "Opening Google"


def open_gmail():
    webbrowser.open("https://mail.google.com")
    return "Opening Gmail"


def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com")
    return "Opening WhatsApp Web"

def open_website(site):

    site = site.lower().strip()

    if "." not in site:
        url = f"https://www.{site}.com"
    else:
        url = f"https://{site}"

    webbrowser.open(url)

    return f"Opening {site}"