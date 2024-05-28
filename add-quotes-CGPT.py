import signal
import sys
import requests
from bs4 import BeautifulSoup as bs
import questionary
from rich.console import Console
from rich.markdown import Markdown
import pandas as pd
from rich.progress import track
from rich.padding import Padding

MARKDOWN = """
# Benventi al gestionale di aforismi (un programma x tuo padre series)

Questo script lavora nel sito ==frasicelebri==: 
- scraping sulle pagine del sito frasicelebri
- visualizza le citazioni
- inserimento nel database (da fare)
---
"""

FRASI_CELEBRI_URL = "https://www.frasicelebri.it/frasi-di/"
console = Console()
md = Markdown(MARKDOWN)
console.print(md)

requests.packages.urllib3.disable_warnings()
pd.set_option("display.max_rows", 500)
pd.set_option("display.max_colwidth", 200)


def signal_handler(sig, frame):
    print("Ctrl+C detected. Exiting gracefully...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main_logic():
    while True:
        author_name = get_author_name()
        author_url = FRASI_CELEBRI_URL + author_name.lower().replace(" ", "-")
        if verify_author_url(author_url, author_name):
            soup = bs(requests.get(author_url, verify=False).text, "html.parser")
            last_page_number = get_last_page_number(soup)
            if last_page_number:
                scrape_multi_page_quotes(author_url, last_page_number)
            else:
                scrape_single_page_quotes(author_url)


def get_author_name():
    while True:
        print(Padding("nome cognome(optional) (Case insensitive)", (1, 2)))
        author_name = questionary.text("Digita il nome di un autore: ").ask()
        if author_name:
            return author_name
        else:
            console.print(Padding("Inserisci un nome! sciocco", (1, 2)))


def verify_author_url(author_url, author_name):
    try:
        response = requests.get(author_url, verify=False)
        response.raise_for_status()
        if questionary.confirm(f"L'autore {author_name} è presente. Procedere?").ask():
            return True
    except requests.exceptions.RequestException:
        console.print(f"La pagina per {author_name} non esiste.")
    return False


def get_last_page_number(soup):
    element = soup.select_one(".fc-pagination ul li.last-page a")
    return element.text if element else None


def scrape_single_page_quotes(author_url):
    page_text = requests.get(author_url, verify=False).text
    blockquotes = bs(page_text, "html.parser").select("blockquote.clearfix")
    quotes = [quote.select_one("span.whole-read-more").text for quote in blockquotes]
    display_quotes(quotes)


def scrape_multi_page_quotes(author_url, last_page_number):
    author_pages = [
        f"{author_url}/?page={i}" for i in range(1, int(last_page_number) + 1)
    ]
    pages_text = [
        requests.get(page, verify=False).text
        for page in track(author_pages, description="Collecting pages...")
    ]
    blockquotes = [
        bs(page, "html.parser").select("blockquote.clearfix") for page in pages_text
    ]
    quotes = [
        quote.select_one("span.whole-read-more").text
        for blockquote in blockquotes
        for quote in blockquote
    ]
    display_quotes(quotes)


def display_quotes(quotes):
    if questionary.confirm("Visualizzare le citazioni dell'autore?").ask():
        print(pd.DataFrame(quotes))


if __name__ == "__main__":
    console.print("Running... Press Ctrl+C to exit.")
    try:
        main_logic()
    except KeyboardInterrupt:
        console.print("KeyboardInterrupt: Exiting...")
