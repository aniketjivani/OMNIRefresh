Fetch and refresh plasma quantities from OMNI data in a Dash 💨 app built with Python 😇

OMNIWeb: https://omniweb.gsfc.nasa.gov/

Retrieving Data From the command line: https://omniweb.gsfc.nasa.gov/html/command_line_sample.txt

`dash_app_pyorbital.ipynb` is not part of our pipeline, its simply to understand how `dcc.Interval` element works. Run in Colab to avoid issues with local PyOrbital installation.

`app.py` is the main file which is part of our pipeline for OMNI (and eventually Deep GP).

To run an app locally (deploy instructions to follow), do `python {app_filename.py}`.