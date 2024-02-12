
from datetime import datetime

ISOFORMAT = "%Y-%m-%dT%H:%M"

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