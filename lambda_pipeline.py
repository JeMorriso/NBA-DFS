import os

# AWS SDK
import boto3
import boto3.session

# this will be used to access Aurora's Data API
from sqlalchemy import create_engine
# awswrangler provides convenient methods for Pandas to AWS DB
import awswrangler as wr

import pandas as pd

from nba_api.stats.static import players


def db(session):
    rds = session.client('rds-data', region_name='us-west-2')

    sql = "insert into Hello (message) values ('hello from local machine')"

    response = rds.execute_statement(
        resourceArn=os.getenv("CLUSTER_ARN"),
        secretArn=os.getenv("SECRET_ARN"),
        database='hello',
        sql=sql
    )
    print(str(response))


def bucket(session):
    s3 = session.resource('s3')

    foo = pd.DataFrame({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
    # don't export to file, return csv string
    csv_str = foo.to_csv()
    # put_object method requires byte stream, not string
    csv_stream = bytes(csv_str.encode('UTF-8'))

    s3.Bucket(os.getenv("S3_BUCKET")).put_object(
        Key='testing.csv', Body=csv_stream)


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

    bucket(session)
    db(session)


if __name__ == "__main__":
    print(os.getenv("S3_BUCKET"))
    driver_fn()
