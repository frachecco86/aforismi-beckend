import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import string
from rich.progress import track
import questionary

requests.packages.urllib3.disable_warnings()

# Generate URLs for each letter
urls = [
    f"https://www.frasicelebri.it/indice/autori/{letter}"
    for letter in string.ascii_lowercase
]

# Scrape and collect authors' names
authors_names = []
authors_hrefs = []

authors = []
for url in urls:
    soup = bs(requests.get(url, verify=False).text, "html.parser")

    for a in track(soup.select("#authors-index > h2 ~ a")):
        name = a.text
        href = a["href"]
        authors.append({"name": name, "href": href})

df = pd.DataFrame(authors)

if questionary.confirm("Scrivere il  il dataframe sul file csv?").ask():
    df.to_csv("frasi_celebri_authors.csv", index=False)


# print(pd.DataFrame(authors_hrefs).head(10))
# pd.DataFrame(authors_names).to_csv("frasi_celebri_authors.csv", index=False)
# pd.DataFrame(authors_hrefs).to_csv("frasi_celebri_authors_hrefs.csv", index=False)


# Prepare data for DataFrame
# authors_data = [
#     {"full_name": name, "by_surname": " ".join(reversed(name.split()))}
#     for name in authors_list
# ]

# # Create and save DataFrame to CSV
# pd.DataFrame(authors_data).to_csv("authors.csv", index=False)

# # Load and display DataFrame for verification
# print(pd.read_csv("authors.csv").columns)
