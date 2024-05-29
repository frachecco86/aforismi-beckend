import re
import questionary
import requests
import pandas as pd


# from prisma import Prisma
from bs4 import BeautifulSoup as bs
from rich.padding import Padding
from rich.progress import track
from rich import print
from rich.console import Console
from rich.markdown import Markdown

import logging
from rich.logging import RichHandler

# FORMAT = "%(message)s"
# logging.basicConfig(
#     level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
# )

# log = logging.getLogger("rich")

# disbale ssl warnings
requests.packages.urllib3.disable_warnings()
# promp libraries

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_colwidth", 200)

MARKDOWN = """
# Benventi al gestionale di aforismi (un programma x tuo padre series 🤩)

Questo script lavora nel sito ==frasicelebri==: 

- scraping sulle pagine del sito frasicelebri
- visualizza le citazioni
- inserimento nel database (da fare)

---
"""

FRASI_CELEBRI_NAME = "frasicelebri.it"
FRASI_CELEBRI_URL = url = "https://www.frasicelebri.it"
AUTHOR_URL = ""

console = Console()
md = Markdown(MARKDOWN)
console.print(md)


# Get frasicelebri authors list
df = pd.read_csv("./frasi_celebri_authors.csv")
authors_list = df["name"].values.tolist()


def keyword_search(items, keyword):
    pattern = re.compile(keyword, re.IGNORECASE)
    authors = [item for item in items if pattern.search(item)]
    return authors


def select_author():
    while True:
        # Keyword to search for
        keyword = questionary.text(
            "inserisci il nome dell'autore o una parola chiave"
        ).ask()
        matching_items = keyword_search(authors_list, keyword)
        author = questionary.select(
            "Scegli l'autore dalla lista",
            choices=matching_items,
        ).ask()
        # author = author_selected.lower().replace(" ", "-")
        # author_url = FRASI_CELEBRI_URL + author
        author_url = FRASI_CELEBRI_URL + df.loc[df["name"] == author, "href"].values[0]
        print(
            Padding(
                f"la pagina autore e' {author_url} ",
                (1, 2),
                style="on blue",
            )
        )

        if questionary.text("Procedere?").ask():
            response = requests.get(author_url, verify=False)
            if response.ok:
                # log.info("response ok")
                requests.get(author_url, verify=False)
                soup = bs(response.text, "html.parser")
                get_author_quotes(soup, author_url)
            else:
                print(
                    Padding(
                        (f"l{author_url} non e' valido o la pagina e' diversa"),
                        (1, 2),
                        style="on red",
                    )
                )
        if not questionary.confirm("Vuoi scegliere un altro autore?").ask():
            break


def get_author_quotes(soup, author_url):
    if soup.select_one(".fc-pagination ul li.last-page a"):
        element = soup.select_one(".fc-pagination ul li.last-page a")
        last_page_number = element.text if element else None
        more_pages = bool(element)
        if more_pages:
            if questionary.confirm(
                f"procedere con lo scraping dell'autore.Sono presenti {last_page_number} pagine "
            ).ask():
                get_multi_page_quotes(author_url, last_page_number)
    else:
        if questionary.confirm("Procedere con lo scraping?").ask():
            get_single_page_quotes(author_url)


def get_single_page_quotes(author_url):
    page_text = requests.get(author_url, verify=False).text
    blockquotes = bs(page_text, features="html.parser").select("blockquote.clearfix")
    quotes = []
    for quote in track(blockquotes, description="Fetching quotes..."):
        quotes.append(quote.select_one("span.whole-read-more").text)

    if questionary.confirm("Visualizzare le citazioni dell'autore?").ask():
        print(pd.DataFrame(quotes))


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
    quotes = []
    for blockquote in blockquotes:
        for quote in track(blockquote):
            selected_quote = quote.select_one("span.whole-read-more")
            if selected_quote:
                quotes.append(selected_quote.text)

    if questionary.confirm("Visualizzare le citazioni dell'autore?").ask():
        print(pd.DataFrame(quotes))


select_author()
