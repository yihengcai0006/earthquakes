# plot_earthquakes.py
# plot_earthquakes.py
from datetime import date
import matplotlib.pyplot as plt
import numpy as np
import json


def get_data():
    """Load earthquake data from the local raw_earthquakes.json file."""
    with open("raw_earthquakes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_year(earthquake):
    """Extract the year in which an earthquake happened."""
    timestamp = earthquake['properties']['time']
    # The time is given in a strange-looking but commonly-used format.
    # To understand it, we can look at the documentation of the source data:
    # https://earthquake.usgs.gov/data/comcat/index.php#time
    # Fortunately, Python provides a way of interpreting this timestamp:
    # (Question for discussion: Why do we divide by 1000?)
    year = date.fromtimestamp(timestamp/1000).year
    return year


def get_magnitude(earthquake):
    """Retrieve the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_magnitudes_per_year(earthquakes):
    """Group magnitudes by year."""
    result = {}
    for quake in earthquakes:
        year = get_year(quake)
        mag = get_magnitude(quake)
        if mag is not None:  
            result.setdefault(year, []).append(mag)
    return result


def plot_average_magnitude_per_year(earthquakes):
    data = get_magnitudes_per_year(earthquakes)
    years = sorted(data.keys())
    avg_mags = [np.mean(data[y]) for y in years]

    plt.figure(figsize=(10, 5))
    plt.plot(years, avg_mags, marker="o")
    plt.xlabel("Year")
    plt.ylabel("Average Magnitude")
    plt.title("Average Earthquake Magnitude per Year")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("average_magnitude_per_year.png")
    plt.show()


def plot_number_per_year(earthquakes):
    data = get_magnitudes_per_year(earthquakes)
    years = sorted(data.keys())
    counts = [len(data[y]) for y in years]

    plt.figure(figsize=(10, 5))
    plt.bar(years, counts)
    plt.xlabel("Year")
    plt.ylabel("Number of Earthquakes")
    plt.title("Earthquake Frequency per Year")
    plt.tight_layout()
    plt.savefig("number_per_year.png")
    plt.show()


# === main program ===
quakes = get_data()['features']

# plot
plot_number_per_year(quakes)
plt.clf()  # Clear the canvas to avoid overlapping images
plot_average_magnitude_per_year(quakes)