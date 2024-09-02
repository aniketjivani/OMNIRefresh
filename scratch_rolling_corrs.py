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

# years_to_plot = [2014, 2015, 2016, 2017]
years_to_plot = [2015, 2016, 2017]

all_figs = []

for year in years_to_plot:
    # filter df_corr_final by year
    df_corr_year = df_corr_final[df_corr_final.index.year == year]

    cme_icme_year = pd.read_csv(f"data/processed_data/cme_icme_{year}.csv")

    # convert columns to datetime values.
    cme_dates = pd.to_datetime(cme_icme_year['CME Date'])
    arrival_times = pd.to_datetime(cme_icme_year['Arrival Time'])

    fig, axes = plt.subplots(6, 1, figsize=(10, 3 * 6))

    for i, col in enumerate(df_corr_year.columns):
        ax = axes[i]
        ax.plot(df_corr_year.index, df_corr_year[col], label=col)
        ax.set_title(col)
        ax.legend(loc='best')

        for cme_date, arrival_time in zip(cme_dates, arrival_times):
            ax.axvline(cme_date, color='red', linestyle='--', label='CME Date')
            ax.axvline(arrival_time, color='green', linestyle='--', label='Arrival Time')

    fig.suptitle(f"Year: {year}", y=1.02)

    plt.tight_layout()
    all_figs.append(fig)

# 
# %% For each 2 day period before and after CME arrival, plot rolling correlations over 10 minute intervals.

# identify 2-3 day periods before and after CME arrival
# for year in years_to_plot:
year = 2016
cme_icme_year = pd.read_csv(f"data/processed_data/cme_icme_{year}.csv")
cme_dates = pd.to_datetime(cme_icme_year['CME Date'])
arrival_times = pd.to_datetime(cme_icme_year['Arrival Time'])

# filter df_corr_final by year, break into subsets based on CME arrival time

df_corr_year = df_corr_final[df_corr_final.index.year == year]
all_figs = []
for cme_date, arrival_time in zip(cme_dates, arrival_times):
    print(f"Year: {year}, CME Date: {cme_date}, Arrival Time: {arrival_time}")
    # filter df_corr_year by cme_date and arrival_time
    df_corr_cme = df_corr_year[(df_corr_year.index >= arrival_time - pd.Timedelta(days=3)) &
                                (df_corr_year.index <= arrival_time + pd.Timedelta(days=1))]

    # remove previous rolling corr columns
    df_corr_cme = df_corr_cme.drop(columns=[col for col in df_corr_cme.columns if '_corr' in col])

    # calculate rolling correlations over 3-hour intervals
    rolling_window = 180
    pairwise_rolling_corr = {f'{col1}_{col2}_corr': df_corr_cme[col1].rolling(rolling_window).corr(df_corr_cme[col2])
                             for i, col1 in enumerate(df_corr_cme.columns)
                             for col2 in df_corr_cme.columns[i + 1:]}
    
    all_roll_corr = pd.DataFrame(pairwise_rolling_corr, index=df_corr_cme.index)

    # Merge all_roll_corr with df_corr_cme (join on index)
    df_corr_cme = df_corr_cme.join(all_roll_corr)

    # Drop NaN correlation values
    df_corr_cme = df_corr_cme.dropna()


    fig, axes = plt.subplots(6, 1, figsize=(10, 3 * 6))

    for i, col in enumerate(df_corr_cme.columns):
        ax = axes[i]
        ax.plot(df_corr_cme.index, df_corr_cme[col], 
                linewidth=0.5,
                label=col)
        ax.set_title(col)
        ax.legend(loc='best')

        ax.axvline(cme_date, color='red', linestyle='--', label='CME Date')
        ax.axvline(arrival_time, color='green', linestyle='--', label='Arrival Time')

    fig.suptitle(f"Year: {year}, CME Date: {cme_date}, Arrival Time: {arrival_time}", y=1.02)

    plt.tight_layout()
    all_figs.append(fig)


# %%
