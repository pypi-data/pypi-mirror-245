from datetime import datetime, timedelta

import numpy as np
import pytz


SECONDS = timedelta(seconds=1)
MINUTES = timedelta(seconds=60)
HOURS = timedelta(seconds=3600)
DAYS = timedelta(days=1)


TIMEZONES = {}
for tz in pytz.all_timezones:
    TIMEZONES[tz] = pytz.timezone(tz)
TIMEZONES[None] = None


def now(tz: str = "UTC"):
    """
    Return a timezone aware datetime of now.
    """
    return datetime.now(tz=TIMEZONES[tz])


def datetime_aware(*args, tz: str = "UTC"):
    """
    How to make a tz-aware datetime.
    """
    return datetime(*args, tzinfo=TIMEZONES[tz])


def datetime_range(start: datetime, end: datetime, interval: timedelta):
    """
    Create an numpy array of datetimes a la numpy.arange.
    """
    dttms, n = [start], 0

    while dttms[-1] < end - interval:
        n += 1
        dttms.append(start + n * interval)

    return np.array(dttms)


def timestamp_to_datetime(timestamp: np.float_, tz: str = "UTC"):
    """
    Return the datetime object given a posix timestamp.
    """
    return datetime(1970, 1, 1, tzinfo=TIMEZONES[tz]) + timestamp * SECONDS


def string_to_datetime(string: str, tz: str = None):
    """
    Return the datetime of a iso-formatted datetime string.
    """
    dttm = datetime.fromisoformat(string)

    if dttm.tzinfo is None and tz is not None:
        dttm = TIMEZONES[tz].localize(dttm)
    else:
        if tz is not None:
            dttm = dttm.astimezone(TIMEZONES[tz])
        else:
            dttm = dttm.replace(tzinfo=None)

    return dttm
