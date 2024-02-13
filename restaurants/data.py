from io import StringIO
from datetime import date

import pandas as pd
import requests

from restaurants.utils import (
    is_isoformat,
    parse_and_tabulate_hours,
    add_24_hours,
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

        # This will make the code below more compact.
        df = self.dataframe

        # Split the iso format into the date and time.
        day, time = datetime_str.split("T")
        day = date.fromisoformat(day)
        weekday = WEEKDAYS[day.weekday()]

        # Find all restaurants open at the given time.
        after_opens1 = df[f"{weekday} {OPENS}"] <= time
        before_closes1 = df[f"{weekday} {CLOSES}"] > time

        # Find the equivalent time for the previous day.
        # For example, Sun at 01:00 become Mon at 25:00
        time_plus_24 = add_24_hours(time)
        previous_day = WEEKDAYS[(day.weekday() - 1) % 7]

        # Find all restaurants open at the transformed time.
        after_opens2 = df[f"{previous_day} {OPENS}"] <= time_plus_24
        before_closes2 = df[f"{previous_day} {CLOSES}"] > time_plus_24

        # Extract the open restaurant from the dataframe.
        open1 = df[after_opens1 & before_closes1]
        open2 = df[after_opens2 & before_closes2]

        # Combine and return the results.
        all_open = set(open1.loc[:,"Restaurant Name"])
        all_open = all_open.union(open2.loc[:,"Restaurant Name"])
        return list(all_open)
