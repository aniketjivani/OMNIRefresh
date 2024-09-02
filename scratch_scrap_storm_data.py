# %% CCMC CME Scoreboard
YEAR_TO_STUDY = 2017
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



url_to_scrap = urljoin("https://kauai.ccmc.gsfc.nasa.gov/CMEscoreboard/PreviousPredictions/", f"{YEAR_TO_STUDY}/")

html_content = fetch_webpage(url_to_scrap)


# %% Parse content
soup = BeautifulSoup(html_content, 'html.parser')
cme_date_tags = soup.find_all('b', string=re.compile(r'CME: *'))

arr_time_tags = soup.find_all('td', string=re.compile(r'(Actual Shock Arrival Time:.*|This CME was not .*)'))
# %% Export content to file

# Create two column dataframe

# for arrival time, if tag is `This CME was not ...`, then arrival time is NaN
# If tag is `Actual Shock Arrival Time: ...`, then arrival time is the date

all_cme_dates = []

for entry in cme_date_tags:
    cme_info = entry.text.split('CME: ')[1].split('-CME')[0]
    cme_date = datetime.strptime(cme_info, '%Y-%m-%dT%H:%M:%S')

    all_cme_dates.append(cme_date)

all_arrival_times = []
for entry in arr_time_tags:
    if 'This CME was not' in entry.text:
        all_arrival_times.append(None)
    else:
        arr_time = entry.text.split('Actual Shock Arrival Time: ')[1]
        all_arrival_times.append(datetime.strptime(arr_time, '%Y-%m-%dT%H:%MZ'))

# dataframe (convert None to NaN)
cme_records_df = pd.DataFrame({'CME Date': all_cme_dates, 'Arrival Time': all_arrival_times})

cme_icme_df = cme_records_df[cme_records_df['Arrival Time'].notnull()]

cme_icme_df.to_csv(f"data/processed_data/cme_icme_{YEAR_TO_STUDY}.csv", index=False)
# %%
