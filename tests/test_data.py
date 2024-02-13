import unittest

from restaurants.data import RestaurantData


class RestaurantDataTest(unittest.TestCase):

    def setUp(self):
        # Load and parse data.
        self.data = RestaurantData()

    def test_data_structure(self):
        """
        Ensure there are 40 rows and 16 columns.
        """
        index = self.data.dataframe.index
        columns = self.data.dataframe.columns
        self.assertEqual(len(index), 40)
        self.assertEqual(len(columns), 16)

    def test_invalid_datetime(self):
        """
        Validate only isoformat is accepted. 
        """
        with self.assertRaises(ValueError) as exc:
            self.data.get_open_restaurants("01-01-2021T12:30")


if __name__ == "__main__":
    unittest.main()
