# Dash App with Python to Fetch and Refresh OMNI Data!
# we will use the interval element from dcc to fetch and refresh data periodically. Right now this will just update the graphs (though you can certainly select a different interval via the traditional callbacks to view past data) but in the future, this will also refresh the Deep GP model predictions.
# See https://dash.plotly.com/live-updates for more help

# Downloading OMNI Data using Python: https://gist.github.com/aniketjivani/1905a061fc86ed7cbe8c1ebd9a147271

from dash import Dash, dcc, html, Input, Output, State
import requests
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import urljoin


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)



