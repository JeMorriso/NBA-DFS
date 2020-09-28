from datetime import date, timedelta, datetime

from sportsreference.nfl.boxscore import Boxscore, Boxscores

from sport import Sport


class NFL(Sport):
    def __init__(self):
        Sport.__init__(self, start_date=date.fromisoformat(
            '2020-09-10'), season=2020)

    def _week_from_date(self, date_):
        return int((date_ - self.start_date).days / 7) + 1

    def get_boxscore(self):
        pass

    def get_boxscores(self, date_):
        # get the week from the date
        week = self._week_from_date(date_)
        games = Boxscores(week, self.season)

        return True
