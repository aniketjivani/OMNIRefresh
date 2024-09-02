# %%
import time
from rich.progress import track
import os
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
import datetime
import requests
from bs4 import BeautifulSoup
# %%
import matplotlib.pyplot as plt
# %%
df = pd.read_pickle("data/processed_data/OMNI_final.pkl")
# %%
rolling_window = 600
# %%
df_final = df[['Proton Density, n/cc', 'Flow speed, km/s', 'B']]

# Rename df_final columns
df_final.columns = ['N', 'U', 'B']

df_final.head()
# %%
pairwise_rolling_corr = {f'{col1}_{col2}_corr': df_final[col1].rolling(rolling_window).corr(df_final[col2])
                         for i, col1 in enumerate(df_final.columns)
                         for col2 in df_final.columns[i+1:]}

all_roll_corr = pd.DataFrame(pairwise_rolling_corr, index=df_final.index)
# %%
# Merge all_roll_corr with df_final (join on index)

df_final = df_final.join(all_roll_corr)

# Drop NaN correlation values

df_corr_final = df_final.dropna()

# %% Plot things: Select data by year / storm and examine correlations. Mark MapTime and CME arrival time.



