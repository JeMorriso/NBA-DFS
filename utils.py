class Utils:
    @classmethod
    def _week_from_date(cls, date_, start_date):
        return int((date_ - start_date).days / 7) + 1

    @classmethod
    def _date_to_sportsreference_str(cls, date_):
        return date_.strftime("%m-%d-%Y")
