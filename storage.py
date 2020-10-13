from abc import ABC, abstractmethod
import os
from io import StringIO
from pathlib import Path

import pandas as pd


class Storage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def dataframe_to_csv(self, df, path):
        pass

    @abstractmethod
    def csv_to_dataframe(self, path):
        pass


class LocalStorage(Storage):
    def __init__(self):
        # add trailing slash to make path compatible with local or s3
        self.dir = f'{str((Path() / Path(os.getenv("LOCAL_DIR")).resolve()))}/'

    def dataframe_to_csv(self, df, path):
        df.to_csv(self.dir + path, header=True, index=False)

    def csv_to_dataframe(self, path):
        return pd.read_csv(self.dir + path)


class S3Storage(Storage):
    def __init__(self, session):
        # boto3 session from user or lambda role
        self.s3 = session.client("s3")
        self.bucket = os.getenv("S3_BUCKET")

    def dataframe_to_csv(self, df, path):
        # don't export to file, return csv string
        csv_str = df.to_csv(header=True, index=False)
        # put_object method requires byte stream, not string
        csv_stream = bytes(csv_str.encode("UTF-8"))

        self.s3.put_object(Bucket=self.bucket, Key=path, Body=csv_stream)

    def csv_to_dataframe(self, path):
        obj = self.s3.get_object(Bucket=self.bucket, Key=path)
        csv_str = obj["Body"].read().decode("UTF-8")

        return pd.read_csv(StringIO(csv_str))
