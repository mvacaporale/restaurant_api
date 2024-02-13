
import re

from datetime import datetime

CLOSES = "Closes"
OPENS = "Opens"
ISOFORMAT = "%Y-%m-%dT%H:%M"
WEEKDAYS = "Mon Tues Wed Thu Fri Sat Sun".split(" ")


def is_isoformat(datetime_str):
    """
    Check if a given datetime str is in the proper isoformat.
    """

    # Attempt to parse the string and return False if it fails.
    try:
        datetime.strptime(datetime_str, ISOFORMAT)
    except ValueError:
        return False

    return True


def parse_and_tabulate_hours(dataframe):
    """
    Parse restaurant hours in the given dataframe and add new columns.
    """

    # Modify a copy of the dataframe
    new_df = dataframe.copy()

    # Add a column for each open and close time for each day of the week,
    # so 14 new columns total (e.g. "Mon Opens" and "Mon Closes").
    for w in WEEKDAYS:
        for c in [OPENS, CLOSES]:
            new_column = w + " " + c
            new_df[new_column] = None

    # Parse the written hours for each restaurant and fill the new columns.
    for index, written_hours in zip(new_df.index, new_df["Hours"]):

        # Each restaurant has different hours listed for different days,
        # separated by "/" (e.g. "Sun 1pm -5pm / Mon-Fri 9am-10pm").
        written_hours = written_hours.replace(" ", "")
        for days_and_hours in written_hours.split("/"):

            # This yeilds a list of days and army formatted hours for those days
            days, hours = parse_days_and_hours(days_and_hours)
            open_time, closed_time = hours

            # Tabulate the open and close times for each day.
            for d in days:
                col1 = f"{d} {OPENS}"
                col2 = f"{d} {CLOSES}"
                new_df.at[index, col1] = open_time
                new_df.at[index, col2] = closed_time

    return new_df


def parse_days_and_hours(days_and_hours):
    """
    Parse hours for a given set of days. This will return a list of days and the
    open and closing times in ary format. For instance, "Mon-Wed 9am-10pm" will
    return ["Mon", "Tues", "Wed"] along with ("09:00", "22:00").
    """

    # Split the days and hours by finding the first numerical value.
    index = re.search(r"\d", days_and_hours).start()
    days_and_ranges = days_and_hours[:index].replace(" ", "")
    times = days_and_hours[index:].replace(" ", "")

    # Split the time range into start and end.
    start_time, end_time = times.split("-")
    start_time, start_am_pm = start_time[:-2], start_time[-2:]
    end_time, end_am_pm = end_time[:-2], end_time[-2:]

    # Expand a range of days (e.g."Mon-Wed" into a list ["Mon", "Tues", "Wed"])
    all_days = expand_weekdays(days_and_ranges)

    # Convert the times into army format.
    army_time_start = convert_to_army_time(start_time, start_am_pm)
    army_time_end = convert_to_army_time(end_time, end_am_pm)

    # If the closing time wraps past midnight, add
    # 24 hrs (e.g. "01:30" becomes "25:30".
    if army_time_end <= army_time_start:
        army_time_end = add_24_hours(army_time_end)

    return all_days, (army_time_start, army_time_end)


def expand_weekdays(days_and_ranges):
    """
    Convert list of weekdays and ranges (e.g. ["Mon-Wed", "Sat"])
    to list of all inclusive weekdays (e.g. ["Mon", "Tues" "Wed", "Sat"], 
    """
    all_days = []
    for d in days_and_ranges.split(","):
        if d in WEEKDAYS:
            all_days.append(d)
        elif "-" in d:
            start, end = d.split("-")
            i, j = WEEKDAYS.index(start), WEEKDAYS.index(end)
            all_days.extend(WEEKDAYS[i: j + 1])

    return all_days


def add_24_hours(ary_time):
    """
    This is a helper function to add 24 hours to an army
    formatted time. This is helpful for closing times
    past midnight. For instance, a place that closes at
    1:30 am can be listed to close at "25:30".
    """
    hour, minute = ary_time.split(":")
    hour = str(int(hour) + 24)
    return f"{hour}:{minute}"
    

def convert_to_army_time(time, am_pm):
    """
    Convert time str (e.g. "12:00" with "am" or "pm") to a string in army time. 
    """
    # Add "00" in case there are no minutes e.g. ("1 pm")
    hour, minute = (time.split(":") + ["00"])[:2]
    am_pm = am_pm.upper()
    standard = datetime.strptime(f"{hour}:{minute} {am_pm}", "%I:%M %p")
    army =  standard.strftime('%H:%M')
    return army
