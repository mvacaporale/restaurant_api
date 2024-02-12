import json
import unittest

from restaurants.app import app
from restaurants.utils import ISOFORMAT


class RestaurantsTest(unittest.TestCase):

    def setUp(self):
            self.app = app.test_client()
            # self.db = db.get_db()

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
        self.assertEqual(
             f"Invalid datetime format. Should be {ISOFORMAT}.",
             message
        )

    def test_get_open_restaurants(self):
        """
        Test for temp dummy output from API.
        """

        payload = {
            "datetime": "2000-10-31T01:30",
        }
        response = self.app.get("/restaurants", query_string=payload)

        data = response.json["data"]
        self.assertEqual(["Store 1", "Store_2"], data)
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()