import numpy as np

from datetime import datetime, timedelta
import pytz
eastern = pytz.timezone('US/Eastern')
import pandas_market_calendars as mcal


def get_prev_market_day(dt):
    """
    Get previous market day, accounting for weekends and market holidays.

    Parameters
    ----------
    dt : datetime.datetime
        Current datetime.

    Returns
    -------
    datetime.datetime
        Previous market day datetime.
    """

    ydt = eastern.normalize(dt - timedelta(1))  # yesterday

    # check if previous day the weekend
    if ydt.weekday() == 5: ydt = eastern.normalize(ydt - timedelta(1))
    elif ydt.weekday() == 6: ydt = eastern.normalize(ydt - timedelta(2))

    # check for holiday
    nyse_holidays = mcal.get_calendar('NYSE').holidays().holidays
    if str(ydt.date()) in np.datetime_as_string(nyse_holidays):
        ydt = eastern.normalize(ydt - timedelta(1))

    # check for weekend again
    if ydt.weekday() == 6: ydt = eastern.normalize(ydt - timedelta(2))

    return ydt


def get_next_market_day(dt):
    """
    Get next market day, accounting for weekends and market holidays.

    Parameters
    ----------
    dt : datetime.datetime
        Current datetime.

    Returns
    -------
    datetime.datetime
        Next market day datetime.
    """

    tdt = eastern.normalize(dt + timedelta(1))  # tomorrow

    # check if next day the weekend
    if tdt.weekday() == 5: tdt = eastern.normalize(tdt + timedelta(2))
    elif tdt.weekday() == 6: tdt = eastern.normalize(tdt + timedelta(1))

    # check for holiday
    nyse_holidays = mcal.get_calendar('NYSE').holidays().holidays
    if str(tdt.date()) in np.datetime_as_string(nyse_holidays):
        tdt = eastern.normalize(tdt + timedelta(1))

    # check for weekend again
    if tdt.weekday() == 5: tdt = eastern.normalize(tdt + timedelta(2))

    return tdt


def get_last_quarter_end(dt):
    """
    Get date of last quarter end.

    Parameters
    ----------
    dt : datetime.datetime
        Current datetime
    datetime.datetime
        Datetime of last quarter end.
    """

    # get current month and year
    month = dt.month
    year = dt.year

    # calculate first day of current quarter
    quarter_start = datetime(year, ((month-1) // 3) * 3 + 1, 1).astimezone(eastern)

    # calculate last day of previous quarter
    last_quarter_end = eastern.normalize(quarter_start - timedelta(1))

    return last_quarter_end
