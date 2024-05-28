# use Vercel database with prisma schema.

MARKDOWN = """
# Benventi al gestionale di aforismi (un programma x tuo padre series 🤩)

Questo script lavora nel sito ==frasicelebri==: 

- scraping sulle pagine del sito frasicelebri
- visualizza le citazioni
- inserimento nel database (da fare)

---
"""


import signal
import sys


def signal_handler(sig, frame):
    print("Ctrl+C detected. Exiting gracefully...")
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Your main program logic goes here
print("Running... Press Ctrl+C to exit.")

import asyncio
from prisma import Prisma
import requests
from bs4 import BeautifulSoup as bs

# disbale ssl warnings
requests.packages.urllib3.disable_warnings()

# promp libraries
import questionary
from rich.text import Text
from rich.padding import Padding
from rich.progress import track
from rich import print
from rich.console import Console
from rich.markdown import Markdown
import pandas as pd

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_colwidth", 200)


FRASI_CELEBRI_NAME = "frasicelebri.it"
FRASI_CELEBRI_URL = url = "https://www.frasicelebri.it/frasi-di/"
AUTHOR_URL = ""

console = Console()
md = Markdown(MARKDOWN)
console.print(md)

# Here you would put your main program logic that you want to keep running until Ctrl+C is pressed


def main_logic():
    while True:

        def get_url_name(author: str):
            AUTHOR_URL = FRASI_CELEBRI_URL + author
            print(Padding(AUTHOR_URL, (1, 2), style="on blue"))
            if questionary.confirm("Verificare presenza url sul sito?").ask():

                check_author_aviability(AUTHOR_URL, author)
            else:
                get_author()
            # question = questionary.confirm("Procedere allo ")

        # get author name
        def get_author():
            print(Padding("nome cognome(optional) (Case insensitive)", (1, 2)))
            author_name = questionary.text("Digita il nome di un autore. ").ask()

            if not author_name:
                print(Padding("Inserisci un nome! sciocco", (1, 2)))
                get_author()
            else:

                author_url = author_name.lower().replace(" ", "-")
                get_url_name(author_url)

        def check_author_aviability(author_url, author):
            try:
                response = requests.get(author_url, verify=False)
                response.raise_for_status()  # Raise an exception for non-200 status codes
            except requests.exceptions.RequestException as e:
                print(f"La pagina non esiste: {e}")
                if questionary.confirm("Vuoi ricominciare?").ask():
                    get_author()
                else:
                    return
            else:
                # Se l;autore esiste nel isto cheidere confemra
                if questionary.confirm(
                    f"L'autore {author} e' presente in {FRASI_CELEBRI_NAME } procedere?"
                ).ask():
                    soup = bs(response.text, "html.parser")
                    get_author_quotes(soup, author_url)
                else:
                    get_author()

        def get_author_quotes(soup, author_url):
            element = soup.select_one(".fc-pagination ul li.last-page a")
            last_page_number = element.text if element else None
            more_pages = bool(element)

            if more_pages:
                if questionary.confirm(
                    f"procedere con lo scraping dell'autore.Sono presenti {last_page_number} pagine "
                ).ask():
                    get_multi_page_quotes(author_url, last_page_number)

                else:
                    get_author()
            else:
                if questionary.confirm("Procedere con lo scraping?"):

                    get_single_page_quotes(author_url)

        def get_single_page_quotes(author_url):
            page_text = requests.get(author_url, verify=False).text

            blockquotes = bs(page_text, features="html.parser").select(
                "blockquote.clearfix"
            )
            quotes = []
            for quote in track(blockquotes, description="Fetching quotes..."):
                quotes.append(quote.select_one("span.whole-read-more").text)

            if questionary.confirm("Visualizzare le citazioni dell'autore?").ask():
                print(pd.DataFrame(quotes))
            else:
                return

        def get_multi_page_quotes(author_url, last_page_number):
            author_pages = [
                f"{author_url}/?page={i}" for i in range(1, int(last_page_number) + 1)
            ]
            # display author page urls
            console.print(author_pages)
            pages_text = [
                requests.get(page, verify=False).text
                for page in track(author_pages, description="collecting pages pages")
            ]
            blockquotes = [
                (bs(page, features="html.parser").select("blockquote.clearfix"))
                for page in pages_text
            ]

            # quotes =  get all quote
            quotes = []
            for blockquote in blockquotes:
                for quote in track(blockquote):
                    quote = quote.select_one("span.whole-read-more").text

                    quotes.append(quote)

            if questionary.confirm("Visualizzare le citazioni dell'autore?").ask():
                print(pd.DataFrame(quotes))
            else:
                get_author()

        get_author()


if __name__ == "__main__":
    print("Running... Press Ctrl+C to exit.")
    try:
        main_logic()

    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
