import pandas as pd


def load_covid_df():
    csv_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    print("Loading COVID-19 Dataset from ", csv_url, end=" ... ")
    df = pd.read_csv(csv_url, sep=",")
    print("Done")
    return df

