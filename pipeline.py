from datetime import timedelta, date

import pandas as pd
from sqlalchemy.exc import IntegrityError, DatabaseError
from sqlalchemy.sql import text

from utils import Utils


def find_and_insert_new_players(srwrapper, db, stats):
    player_ids = set(stats.index)
    db_players = db.sql_to_dataframe("select * from player")
    db_player_ids = set(db_players["sportsreference_id"])
    players_not_in_db_ids = list(player_ids - db_player_ids)
    players_not_in_db = srwrapper.get_players_info(players_not_in_db_ids)
    try:
        db.dataframe_to_sql(
            players_not_in_db, "player", index=True, index_label="sportsreference_id"
        )
    except IntegrityError:
        print("Should never reach here!")
    except DatabaseError:
        print("Should never reach here!")


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


def swap_team_abbreviations_for_ids_player_stats(db, stats, categories):
    teams = db.sql_to_dataframe("select id, abbreviation from team")

    stats["player_id"] = stats.index
    stats = stats.merge(teams, left_on="team", right_on="abbreviation").rename(
        columns={"id": "team_id"}
    )
    stats = stats.merge(teams, left_on="opponent", right_on="abbreviation").rename(
        columns={"id": "opponent_id"}
    )

    stats = stats.set_index("player_id")
    return stats[["game_id", "team_id", "opponent_id"] + list(categories)]


def swap_player_and_game_id_types(db, stats, categories):
    stats = stats.rename(columns={"game_id": "g_sr_id"})
    db_players = db.sql_to_dataframe("select id, sportsreference_id from player")
    db_players.rename(
        columns={"id": "player_id", "sportsreference_id": "p_sr_id"}, inplace=True
    )
    game_sportsreference_ids = tuple(set(stats["g_sr_id"]))

    # Aurora sqlalchemy implementation does not accept tuples as parameters, it fails
    # with AttributeError. Cannot get it to work with dict params. So use sqlalchemy
    # query, then create dataframe from result.
    # TODO: don't need to be using 'text' object here. Could use
    # sqlalchemy.sql.expression.select
    params = {id: id for id in game_sportsreference_ids}
    query = text(
        f"""
        select id as game_id, sportsreference_id as g_sr_id, home_id, away_id from game
        where sportsreference_id in (
            {','.join([f':{id}' for id in params])}
        )
    """
    )

    # keys fail to return the correct names using the AuroraDB API.
    _keys, rows = db.execute_query(query, params)
    db_games = pd.DataFrame(rows, columns=["game_id", "g_sr_id", "home_id", "away_id"])

    stats = db_players.join(stats, on="p_sr_id")
    stats = db_games.join(stats.set_index("g_sr_id"), on="g_sr_id")
    return stats[list(categories) + ["player_id", "game_id", "team_id", "opponent_id"]]


def insert_player_stats(srwrapper, db, start_date=None, end_date=None):
    if start_date is None:
        start_date = srwrapper.start_date
    if end_date is None:
        end_date = date.today() + timedelta(days=1)

    for date_ in Utils._date_range(
        start_date, end_date, interval=srwrapper.time_interval
    ):
        games = srwrapper.get_games_info(date_)
        games = swap_team_abbreviations_for_ids(db, games)
        try:
            db.dataframe_to_sql(games, "game")
        except IntegrityError:
            print("already inserted games")
        except DatabaseError:
            print("already inserted games")

        try:
            stats = srwrapper.get_players_game_stats(date_)
        except KeyError:
            print("the game has not been played yet.")
            continue

        find_and_insert_new_players(srwrapper, db, stats)

        stats = swap_team_abbreviations_for_ids_player_stats(
            db, stats, srwrapper.categories
        )
        stats = swap_player_and_game_id_types(db, stats, srwrapper.categories)
        try:
            db.dataframe_to_sql(stats, "player_stats")
        except IntegrityError:
            print("already inserted stats")
        except DatabaseError:
            print("already inserted games")


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


def clean_teams_fanduel(players):
    players["team"].replace("JAC", "JAX", inplace=True)


def clean_names(players):
    players["name"] = players["name"].str.lower().str.replace(".", "")
    players["name"] = players["name"].apply(lambda x: " ".join(x.split(" ")[:2]))


def clean_fanduel_players(players):
    players.columns = map(str.lower, players.columns)
    players = players.rename(columns={"nickname": "name", "id": "contest_id"})
    players["fanduel_id"] = players["contest_id"].apply(lambda x: int(x.split("-")[-1]))
    clean_names(players)
    clean_teams_fanduel(players)
    return players


def match_players_with_csv(srwrapper, db, storage, fanduel_players):
    players_to_match = db.sql_to_dataframe(
        "select * from player where fanduel_id is null"
    )
    players_to_match = players_to_match.drop(columns="fanduel_id")
    clean_names(players_to_match)

    ids = {}
    for _, p in players_to_match.iterrows():
        match = try_match(p, fanduel_players, srwrapper)
        if match is not None:
            ids[p["id"]] = match["fanduel_id"]

    matched_players = players_to_match.join(
        pd.DataFrame.from_dict(ids, orient="index", columns=["fanduel_id"]),
        on="id",
        how="inner",
    )

    db.update_player_table(matched_players)


def model_and_output_to_csv(db, model, storage, output_path, fanduel_players):
    query = text(
        """
    select 	g.date_ as date,
    t.abbreviation as team,
    o.abbreviation as opponent,
    p.name,
    p.position,
    p.fanduel_id,
    s.*
    from player_stats s
    join team t on t.id = s.team_id
    join team o on o.id = s.opponent_id
    join game g on g.id = s.game_id
    join player p on p.id = s.player_id
    where p.fanduel_id is not null
    """
    )
    keys, rows = db.execute_query(query)
    # Hacky: In case of AuroraDB, returned columns are not named correctly. First
    # element named 'abbreviation' refers to team, and second to opponent
    try:
        keys[keys.index("date_")] = "date"
        keys[keys.index("abbreviation")] = "team"
        keys[keys.index("abbreviation")] = "opponent"
    except ValueError:
        pass

    teams = db.sql_to_dataframe("select * from team")

    model_output = model.model(pd.DataFrame(rows, columns=keys), teams, fanduel_players)
    storage.dataframe_to_csv(model_output, output_path)


def scrape(srwrapper, db, start_date=None, end_date=None):
    if start_date is None:
        start_date = srwrapper.start_date
    if end_date is None:
        end_date = date.today() + timedelta(days=1)

    insert_player_stats(srwrapper, db, start_date=start_date, end_date=end_date)


def model(srwrapper, db, model, storage, input_path, output_path):
    fanduel_players = clean_fanduel_players(storage.csv_to_dataframe(input_path))
    match_players_with_csv(srwrapper, db, storage, fanduel_players)
    model_and_output_to_csv(db, model, storage, output_path, fanduel_players)


def scrape_and_model(
    srwrapper,
    db,
    model,
    storage,
    input_path,
    output_path,
    start_date=None,
    end_date=None,
):
    scrape(srwrapper, db, start_date=start_date, end_date=end_date)
    model(srwrapper, db, model, storage, input_path, output_path)


# def driver_fn(
#     srwrapper,
#     db,
#     model,
#     storage,
#     input_path,
#     output_path,
#     start_date=None,
#     end_date=None,
# ):
#     if start_date is None:
#         start_date = srwrapper.start_date
#     if end_date is None:
#         end_date = date.today() + timedelta(days=1)

#     insert_player_stats(srwrapper, db, start_date, end_date)

#     fanduel_players = clean_fanduel_players(storage.csv_to_dataframe(input_path))
#     match_players_with_csv(srwrapper, db, storage, fanduel_players)

#     model_and_output_to_csv(db, model, storage, output_path, fanduel_players)


# if __name__ == "__main__":
#     # driver_fn()
#     pass
