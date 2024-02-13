import unittest

from restaurants.utils import (
    parse_days_and_hours,
    convert_to_army_time,
    expand_weekdays,
    is_isoformat,
    add_24_hours,
)


class UtilsTest(unittest.TestCase):

    def test_parse_days_and_hours(self):

        # List test cases: input vs expected output.
        test_cases = [
            ("Thu-Fri 5 pm - 1:30 am", (["Thu", "Fri"], ("17:00", "25:30"))),
            ("Mon 11:30 am - 10 pm", (["Mon"], ("11:30", "22:00"))),
            ("Mon, Tues 1 am - 10 pm", (["Mon", "Tues"], ("01:00", "22:00"))),
            ("Mon 12 am - 12 am", (["Mon"], ("00:00", "24:00"))),
            ("Mon-Wed, Sat 11 am - 12 pm",
                (["Mon", "Tues", "Wed", "Sat"], ("11:00", "12:00"))),
        ]
        for input, expected in test_cases:
            out = parse_days_and_hours(input)
            days_open, (open_time, close_time) = out
            self.assertEqual(days_open, expected[0])
            self.assertEqual(open_time, expected[1][0])
            self.assertEqual(close_time, expected[1][1])

    def test_convert_to_army_time(self):

        # List test cases: input vs expected output.
        test_cases = [
            ("2:30 am", "02:30"),
            ("10 pm", "22:00"),
            ("1 am", "01:00"),
            ("12 pm", "12:00"),
            ("12:30 am", "00:30"),
        ]
        for input, expected in test_cases:
            hour_min, am_pm = input.split(" ")
            out = convert_to_army_time(hour_min, am_pm)
            self.assertEqual(out, expected)

    def test_expand_weekdays(self):

        # List test cases: input vs expected output.
        test_cases = [
            ("Mon-Wed,Sat", ["Mon", "Tues", "Wed", "Sat"]),
            ("Tues-Thu,Sat-Sun", ["Tues", "Wed", "Thu", "Sat", "Sun"]),
            ("Sat", ["Sat"]),
            ("Mon,Sat", ["Mon", "Sat"]),
        ]
        for input, expected in test_cases:
            out = expand_weekdays(input)
            self.assertEqual(out, expected)

    def test_add_24_hours(self):

        # List test cases: input vs expected output.
        test_cases = [
            ("00:00", "24:00"),
            ("01:30", "25:30"),
            ("12:00", "36:00"),
        ]
        for input, expected in test_cases:
            out = add_24_hours(input)
            self.assertEqual(out, expected)

    def test_check_isoformat(self):

        # List test cases: input vs expected output.
        test_cases = [
            ("2024-02-08T23:59", True),
            ("2024-02-08T25:59", False),
            ("2024-02-08T23:40:30", False),
        ]
        for input, expected in test_cases:
            out = is_isoformat(input)
            self.assertEqual(out, expected)



if __name__ == "__main__":
    unittest.main()
