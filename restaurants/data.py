import requests
from io import StringIO
from datetime import date

import pandas as pd

from restaurants.utils import (
    is_isoformat,
    parse_and_tabulate_hours,
    CLOSES,
    OPENS,
    WEEKDAYS,
)


DATA_URL = (
    "https://gist.githubusercontent.com/sharpmoose/d25487b913a08f6a6e6059c07035"
    "a041/raw/ad6142a604f7427572e186ed4bf9c083f8155536/restaurants.csv"
)


def download_csv(url):
    """
    Download raw csv data from url.
    """
    response = requests.get(url)

    if response.status_code == 200:
        # Assuming the CSV is UTF-8 encoded, modify the encoding if necessary
        csv_data = StringIO(response.text)
    else:
        print(f"Failed to download CSV. Status code: {response.status_code}")

    return csv_data


class RestaurantData:

    def __init__(self):
        self.dataframe = self.get_restaurant_data()

    def get_restaurant_data(self):
        """
        Download restaurant data and tabulate the open and closing times given
        the written hours.
        """
        csv_data = download_csv(DATA_URL)
        df = pd.read_csv(csv_data, sep=",")
        parsed_df = parse_and_tabulate_hours(df)
        return parsed_df

    def get_open_restuarants(self, datetime_str):
        """
        Identify open restaurants given an isoformatted datetime string.
        """

        if not is_isoformat(datetime_str):
            raise ValueError("Expected 'datetime_str' str in isoformat.")

        day, time = datetime_str.split("T")
        day = date.fromisoformat(day)
        weekday = WEEKDAYS[day.weekday()]
        after_opens = self.dataframe[f"{weekday} {OPENS}"] < time
        before_closes = self.dataframe[f"{weekday} {CLOSES}"] > time

        all_open = self.dataframe[after_opens & before_closes]
        return list(all_open.loc[:,"Restaurant Name"])
