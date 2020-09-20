import os

# AWS SDK
import boto3
import boto3.session

from Model import Model
from DB import DB
from NBA import NBA
from Storage import Storage


def driver_fn(event=None, context=None):

    # LAMBDA_TASK_ROOT environment variable does not exist locally
    is_lambda = os.environ.get('LAMBDA_TASK_ROOT')

    # on local machine
    if not is_lambda:
        # boto3 will look in credentials file, and environment variables for access key id and secret
        session = boto3.session.Session(profile_name="nba-dfs")
    else:
        # on lambda it's using the role assigned to the Lambda function
        session = boto3.session.Session()

    nba = NBA()
    db = DB(session)
    model = Model()
    storage = Storage(session)

    boxscores = nba.iterate_games(nba.get_boxscore)
    db.dataframe_to_sql(boxscores)
    # get relevant data from db for model
    model_data = db.sql_to_dataframe('', None)
    model_outcome = model.model_fn(model_data)
    storage.to_csv(model_outcome, '')


if __name__ == "__main__":
    driver_fn()
