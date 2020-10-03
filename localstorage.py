import os

import pandas as pd

from storage import Storage


class LocalStorage(Storage):
    def __init__(self):
        self.dir = os.getenv("LOCAL_DIR")

    def csv_to_dataframe(self, path):
        return pd.read_csv(self.dir + path)

    def dataframe_to_csv(self, df, path):
        df.to_csv(self.dir + path)
