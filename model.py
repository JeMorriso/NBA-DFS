import pandas as pd


class Model:
    def __init__(self):
        pass

    def pick_players(self, position, fanduel_players, count=1):
        ids = []
        i = 0
        while i < count:
            try:
                # squeeze to convert 1 dimensional dataframe into series
                match = fanduel_players[
                    fanduel_players["fanduel_id"]
                    == position.sample(replace=True).squeeze()["fanduel_id"]
                ][["contest_id", "name"]].squeeze()

                ids.append((match["name"], match["contest_id"]))
                i += 1
            except KeyError:
                pass
        return ids

    def pick_team_defense(self, teams):
        return teams.sample(replace=True).squeeze()["abbreviation"]

    # crunch some numbers, return dataframe
    def model(self, stats, team_stats, fanduel_players, count=150):
        qb = stats[stats["position"] == "QB"]
        rb = stats[stats["position"] == "RB"]
        wr = stats[stats["position"] == "WR"]
        te = stats[stats["position"] == "TE"]
        flex = stats[stats["position"].isin(["RB", "WR", "TE"])]
        def_ = team_stats

        # Contains tuples of (player name, player contest id) for each DFS lineup.
        # Name included for debugging purposes
        output_list = []
        for i in range(count):
            output_list.append([])
            output_list[i].extend(self.pick_players(qb, fanduel_players))
            output_list[i].extend(self.pick_players(rb, fanduel_players, count=2))
            output_list[i].extend(self.pick_players(wr, fanduel_players, count=3))
            output_list[i].extend(self.pick_players(te, fanduel_players))
            output_list[i].extend(self.pick_players(flex, fanduel_players))
            # duplicate selected defense to make list comprehension easier
            selected_defense = self.pick_team_defense(def_)
            output_list[i].append((selected_defense, selected_defense))

        return pd.DataFrame(
            [[x[1] for x in y] for y in output_list],
            columns=["QB", "RB", "RB", "WR", "WR", "WR", "TE", "FLEX", "DEF"],
        )
