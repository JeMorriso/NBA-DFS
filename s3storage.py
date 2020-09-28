import os

import pandas as pd

from storage import Storage


class S3Storage(Storage):
    def __init__(self, session, bucket=None):
        # boto3 session from user or lambda role
        self.s3 = session.resource('s3')

        if bucket is None:
            self.bucket = os.getenv('S3_BUCKET')
        else:
            self.bucket = bucket

    def to_csv(self, df, path):
        pass
        # dump model generated rosters to csv

        # foo = pd.DataFrame({'x': [1, 2, 3], 'y': ['a', 'b', 'c']})
        # # don't export to file, return csv string
        # csv_str = foo.to_csv()
        # # put_object method requires byte stream, not string
        # csv_stream = bytes(csv_str.encode('UTF-8'))

        # s3.Bucket(os.getenv("S3_BUCKET")).put_object(
        #     Key='testing.csv', Body=csv_stream)
