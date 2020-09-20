import os

# this will be used to access Aurora's Data API
from sqlalchemy import create_engine
# awswrangler provides convenient methods for Pandas to AWS DB
import awswrangler as wr


class DB:
    def __init__(self, session):
        pass

    def dataframe_to_sql(self, df):
        pass

    # old code
    def insert(self, session):
        rds = session.client('rds-data', region_name='us-west-2')

        sql = "insert into Hello (message) values ('hello from local machine')"

        response = rds.execute_statement(
            resourceArn=os.getenv("CLUSTER_ARN"),
            secretArn=os.getenv("SECRET_ARN"),
            database='hello',
            sql=sql
        )
        print(str(response))

    def sql_to_dataframe(self, query, table):
        # use aws wrangler read_sql_query to read into dataframe
        pass
