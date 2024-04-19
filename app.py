# Dash App with Python to Fetch and Refresh OMNI Data!
# we will use the interval element from dcc to fetch and refresh data periodically. Right now this will just update the graphs (though you can certainly select a different interval via the traditional callbacks to view past data) but in the future, this will also refresh the Deep GP model predictions.
# See https://dash.plotly.com/live-updates for more help

# Downloading OMNI Data using Python: https://gist.github.com/aniketjivani/1905a061fc86ed7cbe8c1ebd9a147271

# what kind of callbacks do we want in the graph?
# 1. Whenever new data is found through the interval component, update the graph, but always showing the last 30 days of data by default. Show graphs for U, Density, Bz, and possibly Dst index? Note that different data are available up to different dates - hopefully this is doesn't need a lot of boilerplate code to handle.

# 2. When the user selects a different date range, update the graph to show the new date range.


from dash import Dash, dcc, html, Input, Output, State, callback
import requests
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import urljoin


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Define the app layout
app.layout = html.Div([
    html.H1("OMNIWeb Data"),
    dcc.DatePickerRange(
        id="date-range-picker",
        start_date=datetime.today() - timedelta(days=7),
        end_date=datetime.today(),
        display_format="YYYY-MM-DD",
        initial_visible_month=datetime.today() - timedelta(days=3),
    ),
    # html.Div(id="live-update-text"),
    dcc.Graph(id="omni-graph"),
    dcc.Interval(id="interval-component", interval=7200 * 1000, n_intervals=0)  # Refresh every hour
])

# @callback(Output('live-update-text', 'children'),
#               Input('interval-component', 'n_intervals'))
# def update_metrics(n):
#     lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
#     style = {'padding': '5px', 'fontSize': '16px'}
#     return [
#         html.Span('Longitude: {0:.2f}'.format(lon), style=style),
#         html.Span('Latitude: {0:.2f}'.format(lat), style=style),
#         html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#     ]

# Note: When n_intervals is 0, show the last 30 days of data. Otherwise, always show the last 30 days of data up to the current date (which may not have changed every interval)

def fetch_omni_data(start_date, end_date, vars):
    url = "https://omniweb.gsfc.nasa.gov/cgi/nx1.cgi"
    params = {
        "activity": "retrieve",
        "res": "hour",
        "spacecraft": "omni2",
        "start_date": start_date,
        "end_date": end_date,
        "vars": vars,
        "scale": "Linear",
        "view": "0",
        "linestyle": "solid",
        "table": "0",
        "imagex": "640",
        "imagey": "480"
    }
    response = requests.get(url, params=params)
    data = response.text.split("\n")[4:-2]  # Remove header and footer lines
    df = pd.DataFrame([row.split() for row in data], columns=["Year", "Day", "Hour"] + [f"Var{i}" for i in vars])
    df[["Year", "Day", "Hour"] + [f"Var{i}" for i in vars]] = df[["Year", "Day", "Hour"] + [f"Var{i}" for i in vars]].astype(float)
    df["DateTime"] = pd.to_datetime(df[["Year", "Day", "Hour"]].assign(Hour=df["Hour"].astype(int) - 1))
    return df


@callback(Output("omni-graph", "figure"), Input("interval-component", "n_intervals"), State("date-range-picker", "start_date"), State("date-range-picker", "end_date"))
def update_graph(n, start_date, end_date):
    vars = [8, 23]  # Specify the variable IDs you want to retrieve
    df = fetch_omni_data(start_date, end_date, vars)

    data = [
        go.Scatter(x=df["DateTime"], y=df[f"Var{var}"], mode="lines", name=f"Variable {var}")
        for var in vars
    ]

    layout = go.Layout(
        title="OMNIWeb Data",
        xaxis=dict(title="Date/Time"),
        yaxis=dict(title="Value")
    )




