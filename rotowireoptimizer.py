import pandas as pd

import requests


def get(
    base_url="https://www.rotowire.com/daily/tables",
    optimizer_url="optimizer-nba.php",
    sport="NBA",
    site="FanDuel",
    type_="main",
    slate="all",
):
    """Access rotowire optimizer raw JSON data.

    Returns:
        Dataframe containing all potentially useful features.
    """
    # https://www.rotowire.com/daily/tables/optimizer-nba.php?sport=NBA&site=FanDuel&projections=&type=main&slate=all

    url = f"{base_url}/{optimizer_url}?sport={sport}&site={site}&projections=&type={type_}&slate={slate}"

    r = requests.get(url)

    drop_columns = [
        "actions",
        "actions_trigger",
        "lock",
        "exclude",
        "like",
        "real_position",
        "position_chooser",
        "pos_chooser_reset",
        "multiplier",
        "salary_custom",
        "proj_third_party_one",
        "proj_third_party_two",
        "proj_custom",
    ]

    projections = pd.DataFrame(r.json()).drop(columns=drop_columns)
    return projections
