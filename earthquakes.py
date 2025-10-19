# The Python standard library includes some functionality for communicating over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import json
import requests


def get_data():
    # With requests, we can ask the web service for the data.
    # Can you understand the parameters we are passing here?
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )

    # The response we get back is an object with several fields.
    # The actual contents we care about are in its text field:
    text = response.text

    # To understand the structure of this text, you may want to save it
    # to a file and open it in VS Code or a browser.
    # See the README file for more information.
    with open("raw_earthquakes.json", "w", encoding="utf-8") as f:
        f.write(text)

    # We need to interpret the text to get values that we can work with.
    # What format is the text in? How can we load the values?
    data = json.loads(text)
    return data

def count_earthquakes(data):
    return len(data["features"])

def get_magnitude(earthquake):
    return earthquake["properties"]["mag"]

def get_location(earthquake):
    lon, lat, _ = earthquake["geometry"]["coordinates"]
    return (lat, lon)

def get_maximum(data):
    features = data["features"]
    strongest = max(features, key=lambda eq: eq["properties"]["mag"] or -999)
    return get_magnitude(strongest), get_location(strongest)


# With all the above functions defined, we can now call them and get the result
data = get_data()
print(f"Loaded {count_earthquakes(data)}")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")