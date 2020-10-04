import pandas as pd
from sqlalchemy.exc import IntegrityError


def find_and_insert_new_players(srwrapper, db, stats):
    player_ids = set(stats.index)
    db_players = db.sql_to_dataframe("select * from player")
    db_player_ids = set(db_players["sportsreference_id"])
    players_not_in_db_ids = list(player_ids - db_player_ids)
    players_not_in_db = srwrapper.get_players_info(players_not_in_db_ids)
    db.dataframe_to_sql(
        players_not_in_db, "player", index=True, index_label="sportsreference_id"
    )


def swap_team_abbreviations_for_ids(db, games):
    # index is modified when merging dataframes, so turn it into a column here instead
    games["sportsreference_id"] = games.index
    teams = db.sql_to_dataframe("select id, abbreviation from team")
    games = games.merge(
        teams, left_on="home_abbreviation", right_on="abbreviation"
    ).rename(columns={"id": "home_id"})
    games = games.merge(
        teams, left_on="away_abbreviation", right_on="abbreviation"
    ).rename(columns={"id": "away_id"})
    return games[["sportsreference_id", "home_id", "away_id", "date_"]]


def swap_player_and_game_id_types(db, stats, categories):
    stats = stats.rename(columns={"game_id": "g_sr_id"})
    db_players = db.sql_to_dataframe(
        "select id as player_id, sportsreference_id as p_sr_id from player"
    )

    game_sportsreference_ids = tuple(set(stats["g_sr_id"]))
    query = f"""
        select id as game_id, sportsreference_id as g_sr_id from game
        where sportsreference_id in ({','.join(['%s'] * len(game_sportsreference_ids))})
    """
    db_games = db.sql_to_dataframe(query, params=game_sportsreference_ids)

    stats = db_players.join(stats, on="p_sr_id")
    stats = db_games.join(stats.set_index("g_sr_id"), on="g_sr_id")
    return stats[list(categories) + ["player_id", "game_id"]]


def insert_player_stats(srwrapper, db, date_):
    games = srwrapper.get_games_info(date_)
    games = swap_team_abbreviations_for_ids(db, games)
    try:
        db.dataframe_to_sql(games, "game")
    except IntegrityError:
        print("already inserted games")

    stats = srwrapper.get_players_game_stats(date_)
    find_and_insert_new_players(srwrapper, db, stats)

    # TODO: add logging, because this will fail if already inserted stats for that day
    try:
        stats = swap_player_and_game_id_types(db, stats, srwrapper.sport.categories)
        db.dataframe_to_sql(stats, "player_stats")
    except IntegrityError:
        print("already inserted stats")


def is_player_on_team(srwrapper, player_id, team):
    players = srwrapper.get_roster(team, slim=True)
    return player_id in players.players.keys()


def try_match(db_player, fd_players, srwrapper):
    potential_match = fd_players[
        (fd_players["name"] == db_player["name"])
        & (fd_players["position"] == db_player["position"])
    ].squeeze()

    # TODO: improve handling, logging
    if not isinstance(potential_match, pd.Series):
        print(db_player)
        return None
    else:
        team = srwrapper.abbreviations[potential_match["team"]]
        return (
            potential_match
            if is_player_on_team(srwrapper, db_player["sportsreference_id"], team)
            else None
        )


def clean_names(players):
    players["name"] = players["name"].str.lower().str.replace(".", "")
    players["name"] = players["name"].apply(lambda x: " ".join(x.split(" ")[:2]))


def match_players_with_csv(srwrapper, db, storage, csv_path):
    players_to_match = db.sql_to_dataframe(
        "select * from player where fanduel_id is null"
    )
    players_to_match = players_to_match.drop(columns="fanduel_id")
    fanduel_players = storage.csv_to_dataframe(csv_path)
    fanduel_players = fanduel_players.rename(columns={"Nickname": "name"})
    fanduel_players.columns = map(str.lower, fanduel_players.columns)
    clean_names(players_to_match)
    clean_names(fanduel_players)
    ids = {}
    for i, p in players_to_match.iterrows():
        match = try_match(p, fanduel_players, srwrapper)
        if match is not None:
            ids[p["id"]] = match["id"].split("-")[1]

    matched_players = players_to_match.join(
        pd.DataFrame.from_dict(ids, orient="index", columns=["fanduel_id"]),
        on="id",
        how="inner",
    )

    db.update_player_table(matched_players)


def driver_fn(srwrapper, db, model, storage, date_, input_path, output_path):
    insert_player_stats(srwrapper, db, date_)
    match_players_with_csv(srwrapper, db, storage, input_path)

    #####################
    # for player
    # pass date
    # boxscores = sport.get_boxscores()
    # db.dataframe_to_sql(boxscores)
    # # get relevant data from db for model
    # model_data = db.sql_to_dataframe('', None)
    # model_outcome = model.model_fn(model_data)
    # storage.to_csv(model_outcome, '')
    pass


if __name__ == "__main__":
    # driver_fn()
    pass
