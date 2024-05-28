import re
import pandas as pd
import questionary


def keyword_search(items, keyword):

    pattern = re.compile(keyword, re.IGNORECASE)
    authors = [item for item in items if pattern.search(item)]
    return authors


# Sample list of strings
df = pd.read_csv("frasi_celebri_authors.csv")
authors_list = df["0"].values.tolist()


def select_author():
    # Keyword to search for
    keyword = questionary.text(
        "inserisci una il nome di un autore o una sua iniziale/keyword"
    ).ask()
    matching_items = keyword_search(authors_list, keyword)
    author_selected = questionary.select(
        "quale autore vuoi scegliere?",
        choices=matching_items,
    ).ask()
    print(author_selected)


select_author()

# Call the function
