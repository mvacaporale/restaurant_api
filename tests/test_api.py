import json
import unittest

from restaurants.app import app
from restaurants.utils import ISOFORMAT


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_missing_parameter(self):
        """
        Test bad request for missing datetime parameter.
        """

        response = self.app.get("/restaurants")
        message = response.json["message"]
        self.assertEqual(400, response.status_code)
        self.assertEqual(
             "Missing required parameter in the query string",
             message["datetime"]
        )

    def test_invalid_isoformat(self):
        """
        Test bad request for invalid datetime formatting.
        """

        payload = {
            "datetime": "2000-10-31T01:30:00",
        }
        response = self.app.get("/restaurants", query_string=payload)

        message = response.json["message"]
        self.assertEqual(400, response.status_code)
        self.assertTrue(f"Invalid datetime format" in message)

    def test_returns_list(self):
        """
        Test to ensure the API returns the correct format.
        """

        payload = {
            "datetime": "2000-10-31T12:00",
        }
        response = self.app.get("/restaurants", query_string=payload)

        data = response.json["data"]
        self.assertTrue(isinstance(data, list))
        self.assertEqual(200, response.status_code)


class GetOpenRestaurantsTest(unittest.TestCase):
    """
    Test cases for the endpoint that retrieves open restaurants.
    """

    def setUp(self):
        self.app = app.test_client()

    def test_open_before_midnight(self):
        """
        Retrieve restaurants open just before midnight on a Friday
        """
        datetime_str = "2024-02-09T23:59"
        payload = {"datetime": datetime_str}
        response = self.app.get("/restaurants", query_string=payload)

        output = response.json["data"]
        expected = [
            "Caffe Luna",
            "The Cheesecake Factory",
            "Bonchon",
            "Taverna Agora",
            "Stanbury",
            "42nd Street Oyster Bar",
            "Seoul 116",
        ]

        self.assertEqual(set(expected), set(output))

    def test_open_before_midnight_on_thurs(self):
        """
        Retrieve restaurants open just before midnight on a Thursday.
        """
        datetime_str = "2024-02-08T23:59"
        payload = {"datetime": datetime_str}
        response = self.app.get("/restaurants", query_string=payload)

        output = response.json["data"]
        expected = [
            "Caffe Luna",
            "Bonchon",
            "Stanbury",
            "42nd Street Oyster Bar",
            "Seoul 116",
        ]
        self.assertEqual(set(expected), set(output))

    def test_open_after_midnight_on_fri(self):
        """
        Retrieve restaurants open just after midnight going into Friday.
        """
        datetime_str = "2024-02-09T00:15"
        payload = {"datetime": datetime_str}
        response = self.app.get("/restaurants", query_string=payload)

        output = response.json["data"]
        expected = [
            "Bonchon",
            "Seoul 116",
        ]
        self.assertEqual(set(expected), set(output))


    def test_open_after_midnight_on_sat(self):
        """
        Retrieve restaurants open at midnight going into Saturday.
        """
        datetime_str = "2024-02-10T00:00"
        payload = {"datetime": datetime_str}
        response = self.app.get("/restaurants", query_string=payload)

        output = response.json["data"]
        expected = [
            "Bonchon",
            "The Cheesecake Factory",
            "Seoul 116",
        ]
        self.assertEqual(set(expected), set(output))

    def test_open_monday_1am(self):
        """
        Retrieve restaurants open monday at 1am.
        """
        datetime_str = "2024-02-12T01:00"
        payload = {"datetime": datetime_str}
        response = self.app.get("/restaurants", query_string=payload)

        output = response.json["data"]
        expected = [
            "42nd Street Oyster Bar",
            "Seoul 116",
        ]
        self.assertEqual(set(expected), set(output))

    def test_open_early_sun(self):
        """
        Retrieve restaurants open early on a Sunday.
        """
        datetime_str = "2024-02-14T09:00"
        payload = {"datetime": datetime_str}
        response = self.app.get("/restaurants", query_string=payload)

        output = response.json["data"]
        expected = [
            "Tupelo Honey",
        ]
        self.assertEqual(set(expected), set(output))

    def test_open_mon_at_noon(self):
        """
        Retrieve restaurants open on a Monday at noon.
        """
        datetime_str = "2024-02-12T12:00"
        payload = {"datetime": datetime_str}
        response = self.app.get("/restaurants", query_string=payload)

        output = response.json["data"]
        not_expected = {
            "Beasley's Chicken + Honey",
            "Bonchon",
            "Death and Taxes",
            "Garland"
        }

        self.assertTrue(not_expected not in set(output))
        self.assertEqual(len(output), 36)


if __name__ == "__main__":
    unittest.main()