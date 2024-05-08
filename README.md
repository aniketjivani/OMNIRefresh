Fetch and refresh plasma quantities from OMNI data in a Dash 💨 app built with Python 😇

OMNIWeb: https://omniweb.gsfc.nasa.gov/

Retrieving Data From the command line: https://omniweb.gsfc.nasa.gov/html/command_line_sample.txt

`dash_app_pyorbital.ipynb` is not part of our pipeline, its simply to understand how `dcc.Interval` element works. Run in Colab to avoid issues with local PyOrbital installation.

`app.py` is the main file which is part of our pipeline for OMNI (and eventually Deep GP).

To run an app locally (deploy instructions to follow), do `python {app_filename.py}`.


SWPC Data Products: https://services.swpc.noaa.gov/products/solar-wind/

Scrap JSON file for latest 7 day plasma quantities (from DSCOVR spacecraft) using curl: 

```bash
curl -H "Accept:json" -X GET https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json -o plasma-7-day.json
```

Scrap using Python:
```python
import urllib.request
import json

with urllib.request.urlopen("https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json") as url:
    data = json.loads(url.read().decode())
    print(data)
```

