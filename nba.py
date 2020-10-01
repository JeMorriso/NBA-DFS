from datetime import date

from sport import Sport


class NBA(Sport):
    def __init__(self):
        categories = {
            "assists",
            "blocks",
            "defensive_rating",
            "defensive_rating",
            "defensive_rebounds",
            "field_goal_attempts",
            "field_goals",
            "free_throw_attempts",
            "free_throws",
            "minutes_played",
            "offensive_rating",
            "offensive_rebounds",
            "personal_fouls",
            "points",
            "steals",
            "three_point_attempts",
            "three_pointers",
            "total_rebounds",
            "turnovers",
            "two_point_attempts",
            "two_pointers",
        }
        start_date = date.fromisoformat("2019-10-22")
        season = 2019
        positions = ["pg", "sg", "sf", "pf", "c"]
        super().__init__(start_date, season, categories, positions)
