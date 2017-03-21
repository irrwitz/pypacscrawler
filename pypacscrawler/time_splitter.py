import datetime
from datetime import timedelta, datetime


def split(time_range):
    """
    Splits a query time range into two.
    For given input '000000-235959' will be split to
    '000000-115959' and '120000-235959'
    :param time_range: start and end time, e.g. '000000-235959'
    :return: two time ranges, e.g. '000000-115959' and '120000-235959'
    """
    start, end = time_range.split('-')
    start_value = datetime.strptime(start, '%H%M%S')
    end_value = datetime.strptime(end, '%H%M%S')

    delta_start = timedelta(hours=start_value.hour, minutes=start_value.minute,
                            seconds=start_value.second)
    delta_end = timedelta(hours=end_value.hour, minutes=end_value.minute,
                          seconds=end_value.second + 1)

    middle = abs(delta_end.total_seconds() - delta_start.total_seconds()) / 2
    middle_left = timedelta(seconds=middle - 1)
    middle_right = timedelta(seconds=middle)
    left = start + '-' + f(middle_left)
    rr = timedelta(middle_right.total_seconds() + middle/2)
    right = f(middle_right) + '-' + f(timedelta(seconds=middle_right.total_seconds() + middle - 1))


    return left, right


def pre(value):
    v = str(value)
    if len(v) == 1:
        v = '0' + v
    return v


def f(time_delta):
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return pre(hours) + pre(minutes) + pre(seconds)
