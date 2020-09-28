from datetime import date, timedelta, datetime

from sportsreference.nfl.boxscore import Boxscore

from sport import Sport


class NFL(Sport):
    def __init__(self):
        datetime.strptime('2020-09-10', '%Y-%m-%d').date()
        Sport.__init__(self, start_date=datetime.strptime(
            '2020-09-10', '%Y-%m-%d').date())

    def _week_from_date(self, date_):
        return int((date_ - self.start_date).days / 7) + 1

    def get_boxscore(self):
        pass

    def get_boxscores(self, date_):
        pass

        # get the week from the date
