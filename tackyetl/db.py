import hashlib
import os
from abc import ABC, abstractmethod

import pandas as pd


class PersistanceLogic(ABC):
    @abstractmethod
    def create(self, *xargs, **kwargs):
        pass

    @abstractmethod
    def read(self, *xargs, **kwargs):
        pass

    @abstractmethod
    def update(self, *xargs, **kwargs):
        pass

    @abstractmethod
    def delete(self, *xargs, **kwargs):
        pass


class StdOut(PersistanceLogic):
    def create(self, data: pd.DataFrame):
        print(data.to_string())

    def read(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class CSVDatabase(PersistanceLogic):
    def __init__(self, metadata_file: str = ".owm_metadata"):
        self.metadata_file = metadata_file
        if not os.path.exists(metadata_file):
            self.entries = pd.DataFrame()
        else:
            self.entries = pd.read_csv(self.metadata_file, header=0, index_col=0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.entries.to_csv(self.metadata_file)

    def create(self, data: pd.DataFrame):
        metadata = data.attrs
        key = hashlib.sha256(
            pd.util.hash_pandas_object(data, index=True).values
        ).hexdigest()
        if not os.path.exists(".store"):
            os.mkdir(".store")
        data.to_csv(f".store/{key}")
        metadata.update({"filename": f".store/{key}"})
        short_key = key[:6]
        self.entries = self.entries.append(pd.DataFrame(metadata, index=[short_key]))

    def read(self, data_id: str) -> pd.DataFrame:
        print(self.entries)
        try:
            return pd.read_csv(self.entries.loc[data_id].filename)
        except ValueError:
            raise ValueError(f"No suck key {data_id}")

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError
