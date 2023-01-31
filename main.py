from bokeh.io import show

from covid_dataset import load_covid_df
from vis_arc_bar_chart import arc_bar_chart

if __name__ == "__main__":
    df_covid = load_covid_df()

    # Keeping data for only last date
    df_covid_current = df_covid[df_covid["date"] == df_covid["date"].max()]

    # Removing unnecessary Columns
    df_covid_current = df_covid_current[["location", "population", "total_cases"]]

    # Filtering only for a few countries
    countries = [
        "Italy",
        "Germany",
        "Vietnam",
        "Brazil",
        "United States",
    ]
    df_covid_current = df_covid_current[df_covid_current["location"].isin(countries)]

    p = arc_bar_chart(
        df=df_covid_current,
        absolute_values_col_name="total_cases",
        total_values_col_name="population",
        id_col_name="location",
        title="COVID-19 Cases : Arc Bar Chart (Total Cases ↦ Arc Length; Total Cases per Capita ↦ Angle)",
    )

    show(p)
