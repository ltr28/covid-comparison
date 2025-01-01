import os

import pandas as pd
from matplotlib import pyplot as plt

COVID_DATA_URL = (
    "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"
)
CSV_FILEPATH = "out/covid_world.csv"


OECD_COUNTRIES = [
    "Australia",
    "Austria",
    "Belgium",
    "Canada",
    "Chile",
    "Colombia",
    "Costa Rica",
    "Czechia",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Iceland",
    "Ireland",
    "Israel",
    "Italy",
    "Japan",
    "South Korea",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Mexico",
    "Netherlands",
    "New Zealand",
    "Norway",
    "Poland",
    "Portugal",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
    "Switzerland",
    "Turkey",
    "United Kingdom",
    "United States",
]


def get_data(force: bool = False) -> pd.DataFrame:
    """
    Retrieves the world covid data eitehr from the local data
    or from the URL.

    Args:
        force: Forces the data from the URL.

    Returns:
        pd.DataFrame: The world data from COVID data.
    """

    if os.path.exists(CSV_FILEPATH) and not force:
        df = pd.read_csv(CSV_FILEPATH)
    else:
        df = pd.read_csv(COVID_DATA_URL)
        df.to_csv(CSV_FILEPATH, index=False)
    df.index = pd.to_datetime(df.date)

    return df.sort_index()


def plot_new_cases_by_country(df: pd.DataFrame):
    """Plots the total new cases of COVID 19

    Args:
        df: The raw data containing the new cases per country

    Returns:
        fig: The new case plot.
    """
    cases_df = df.query("date > '2024-01-01' & date <= '2025-01-01'")
    cases_df = cases_df.rename(
        columns={
            "new_cases_smoothed_per_million": "New Cases Per Day Per Million",
        },
    )

    fig, ax = plt.subplots(layout="constrained")
    cases_groupby = cases_df.groupby("location")["New Cases Per Day Per Million"]
    cases_groupby.plot(
        ax=ax,
        rot=90,
    )
    fig.legend(loc="outside lower center", ncols=4)

    return fig


def main():
    df = get_data()
    oecd_data = df[df["location"].isin(OECD_COUNTRIES)]
    fig = plot_new_cases_by_country(oecd_data)
    fig.savefig("out/oecd.png", bbox_inches='tight')

if __name__ == "__main__":
    main()
