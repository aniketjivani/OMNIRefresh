# CCMC CME Scoreboard
# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from urllib.parse import urljoin
import re
# %%
def fetch_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"An error occurred while fetching the webpage: {e}")
        return None
# %%

YEAR_TO_STUDY = 2014

url_to_scrap = urljoin("https://kauai.ccmc.gsfc.nasa.gov/CMEscoreboard/PreviousPredictions/", f"{YEAR_TO_STUDY}/")

html_content = fetch_webpage(url_to_scrap)


# %% Parse content
soup = BeautifulSoup(html_content, 'html.parser')
cme_date_tags = soup.find_all('b', string=re.compile(r'CME: *'))


# %% Export content to file