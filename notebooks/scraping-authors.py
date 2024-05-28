# %%
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import string


letters = string.ascii_lowercase
urls = []
authors_list = []

# %%
# get all authros urls
for l in letters:
    urls.append(f"https://www.frasicelebri.it/indice/autori/{l}")

# get list all authors
for url in urls:
    r = requests.get(url).text
    soup = bs(r)
    authors = soup.select("#authors-index > h2 ~ a")
    for a in authors:
        author = a.text
        authors_list.append(author)

# %%
authors_df = []
for name in authors_list:
    name_splitted = name.split(" ")
    by_surname = list(reversed(name_splitted))
    authors_df.append({"full_name": name, "by_surname": " ".join(by_surname)})


dataframe = pd.DataFrame(authors_df)

csv_file = "authors.csv"
dataframe.to_csv(csv_file, index=False)
data = pd.read_csv(csv_file)
# #mostra tutto il dataframe
data.columns

# %%
