MARKDOWN = """
# Benventi al gestionale di aforismi (un programma x tuo padre series 🤩)

Questo script lavora nel sito ==frasicelebri==:

1. Converte l'input nel formato url corrispondente(es. Roberto Benigni-> roberto-benigni)
2. Se la pagina esiste nel sito controlla se e' gia stata inserita nel database
3. Se non e' stata inserita inseriesce le citazioni nel database 
4. Visualizza i record inseriti nel database 

---
"""

import time
import typer
from rich.prompt import Prompt
from rich.text import Text
from rich.padding import Padding
from rich.progress import track
from rich import print
from rich.console import Console
from rich.markdown import Markdown

FRASI_CELEBRI_URL = url = "https://www.frasicelebri.it/frasi-di/"


def main():
    console = Console()
    md = Markdown(MARKDOWN)
    console.print(md)
    get_author_name()


def get_author_name():
    author_name = Prompt.ask(
        "Digita il nome di un autore [italic red](nome cognome) case insensitive[/italic red]"
    )
    if not author_name:
        print(Padding("Inserisci un nome! sciocco", (1, 2), style="on red"))
        get_author_name()
    else:
        print(f"Hello {author_name}")
        author_url = author_name.lower().replace(" ", "-")
        get_url_name(author_url)


def get_url_name(author: str):
    site_url = FRASI_CELEBRI_URL + author
    print(Padding(site_url, (1, 2), style="on blue"))
    # print(f"[bold]Il l'author url e; {author_url}[/bold]")

    # for i in track(range(20), description="Processing..."):
    #     time.sleep(1)  # Simulate work being done


if __name__ == "__main__":
    typer.run(main)
