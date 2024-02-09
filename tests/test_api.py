import json
import unittest

from restaurants.app import app


class RestaurantsTest(unittest.TestCase):

    def setUp(self):
            self.app = app.test_client()
            # self.db = db.get_db()

    def test_get_datetime(self):

        payload = {
            "datetime": "2000-10-31T01:30:00",
        }

        response = self.app.get("/restaurants", query_string=payload)#, headers=headers)

        self.assertEqual("2000-10-31T01:30:00", response.json["data"])
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()