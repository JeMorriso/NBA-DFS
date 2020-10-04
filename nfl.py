from datetime import date

from sport import Sport


class NFL(Sport):
    def __init__(self):
        categories = {
            "completed_passes",
            "attempted_passes",
            "passing_yards",
            "passing_touchdowns",
            "interceptions_thrown",
            "times_sacked",
            "quarterback_rating",
            "rush_attempts",
            "rush_yards",
            "rush_touchdowns",
            "times_pass_target",
            "receptions",
            "receiving_yards",
            "receiving_touchdowns",
            "kickoff_return_touchdown",
            "punt_return_touchdown",
            "fumbles_lost",
            "fumbles_recovered_for_touchdown",
            "field_goals_made",
            "extra_points_made",
        }
        start_date = date.fromisoformat("2020-09-10")
        season = 2020
        positions = ["QB", "RB", "WR", "TE"]
        super().__init__(start_date, season, categories, positions)
