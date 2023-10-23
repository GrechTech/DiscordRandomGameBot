# From https://github.com/ralacerda/f1next/
from datetime import datetime, timedelta
from math import ceil, floor
from pathlib import Path

import appdirs
import requests_cache
import requests
from dateutil import tz

# List of possible events
events = [
    "Race",
    "Qualifying",
    "FirstPractice",
    "SecondPractice",
    "ThirdPractice",
    "Sprint",
]


def get_json(force_download: bool) -> dict:
    """A function that returns information about the next round.

    It sets up a cache file for requests
    If force_download is True, it deletes the cache first
    It returns only the dictionary with information about the next round
    """

    cache_dir = appdirs.user_cache_dir("f1next", "f1next")
    cache_file = "f1next_cache"
    cache_path = Path(cache_dir, cache_file)

    request = requests_cache.CachedSession(
        str(cache_path), expire_after=timedelta(hours=6)
    )
    if force_download:
        request.cache.clear()
    api_url = "https://ergast.com/api/f1/current/next.json"

    try:
        response = request.get(api_url)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Connection error")
        request.cache.clear()
        exit(1)
    except requests.exceptions.RequestException:
        print("Error downloading data")
        request.cache.clear()
        exit(1)
    return response.json()["MRData"]["RaceTable"]["Races"][0]


def get_countdown_string(time_left: timedelta) -> str:
    """This function produces a string based on
    the time left for the event.

    It takes a `timedelta` object and returns a string
    with days, hours and minutes.
    """

    countdown_string = ""

    # `deltatime` objects only includes days and seconds
    # , so we calculate hours and minutes ourselves
    # rounding down hours and rounding up minutes
    countdown_time = {
        "day": time_left.days,
        "hour": floor(time_left.seconds / (60 * 60)),
        "minute": ceil((time_left.seconds / 60) % 60),
    }

    for unit, amount in countdown_time.items():
        # We only print if the amount is higher than 0
        if amount > 0:
            countdown_string += f"{amount} {unit}"
            # If amount is higher than 1, we include the "s" for plural
            countdown_string += "s " if amount > 1 else " "

    return countdown_string


def get_event_datetime(event_date: str, event_time: str) -> datetime:
    """A helper function that returns a timezone aware datetime.

    It transforms a date string and a time string into
    a datetime object, with UTC as the timezone
    """

    datetime_format = "%Y-%m-%d %H:%M:%S"
    datetime_string = " ".join([event_date, event_time[:-1]])
    event_datetime = datetime.strptime(datetime_string, datetime_format)
    event_datetime = event_datetime.replace(tzinfo=tz.UTC)
    return event_datetime


def custom_output():

    next_round = get_json(True)

    # Date of the next round refers to the race date
    gp_events = {"Race": get_event_datetime(next_round["date"], next_round["time"])}

    # Other events are in their own dictionaries
    for key in events:
        # We need to check the key because not all weekends have Sprint
        # or Third Practice
        if key in next_round:
            gp_events[key] = get_event_datetime(
                next_round[key]["date"], next_round[key]["time"]
            )

    # We sort the dictionary because events are not always the same order
    # Mainly, Second Practice is not always right after First Practice
    gp_events = dict(sorted(gp_events.items(), key=lambda v: v[1]))

    # current_datetime is used both in schedule and countdown options
    current_datetime = datetime.now().replace(tzinfo=tz.gettz())

    # Looking for the first event that has not started yet
    for event_name, event_datetime in gp_events.items():
        if event_datetime > current_datetime:

            # Add a space before Practice
            if "Practice" in event_name:
                event_name = event_name[:-8] + " " + event_name[-8:]

            return_string = event_name + " for the " + next_round[
                "raceName"] + " will start in " + get_countdown_string(event_datetime - current_datetime)
            # Break to not print other events
            break
    # If the for loop doesn't break
    else:
        return_string = "The " + next_round["raceName"] + " started " + get_countdown_string(
            current_datetime - gp_events['Race']) + " ago"

    return return_string
