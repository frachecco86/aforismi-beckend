import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import string

requests.packages.urllib3.disable_warnings()

# Generate URLs for each letter
urls = [
    f"https://www.frasicelebri.it/indice/autori/{letter}"
    for letter in string.ascii_lowercase
]

# Scrape and collect authors' names
authors_list = []
for url in urls:
    soup = bs(requests.get(url, verify=False).text, "html.parser")
    authors_list.extend([a.text for a in soup.select("#authors-index > h2 ~ a")])


pd.DataFrame(authors_list).to_csv("frasi_celebri_authors.csv", index=False)

# Prepare data for DataFrame
# authors_data = [
#     {"full_name": name, "by_surname": " ".join(reversed(name.split()))}
#     for name in authors_list
# ]

# # Create and save DataFrame to CSV
# pd.DataFrame(authors_data).to_csv("authors.csv", index=False)

# # Load and display DataFrame for verification
# print(pd.read_csv("authors.csv").columns)
