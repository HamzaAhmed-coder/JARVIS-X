import webbrowser
import urllib.parse


def google_search(query):

    url = (
        "https://www.google.com/search?q="
        + urllib.parse.quote(query)
    )

    webbrowser.open(url)

    return f"Searching Google for '{query}'"


def google_news(query):

    url = (
        "https://news.google.com/search?q="
        + urllib.parse.quote(query)
    )

    webbrowser.open(url)

    return f"Searching latest news about '{query}'"