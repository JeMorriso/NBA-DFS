from datetime import timedelta
from enum import Enum
import math


class TimeInterval(Enum):
    DAY = 1
    WEEK = 7


class Utils:
    @classmethod
    def _week_from_date(cls, date_, start_date):
        return int((date_ - start_date).days / 7) + 1

    @classmethod
    def _date_to_sportsreference_str(cls, date_):
        return date_.strftime("%m-%d-%Y")

    @classmethod
    def _date_range(cls, start_date, end_date, interval=TimeInterval.DAY):
        return [
            start_date + timedelta(i) * interval.value
            for i in range(math.ceil((end_date - start_date).days / interval.value))
        ]
