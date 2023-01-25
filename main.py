import pandas as pd
from vis_circular_bar_chart import circular_bar_chart
from bokeh.palettes import Category10 as palette

def load_COVID_Dataset():
    csv_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(csv_url, sep=",")
    return df

if __name__ == "__main__":
    countries = [
        "India",
        "Germany",
        "United States",
    ]
    countries_superset = [
        "India", "Germany", "United States", "Italy", "China", "Brazil", "Australia", "France", "Vietnam", "New Zealand"
        ]
    colors = palette[len(countries_superset)]
    print("Hello World")
