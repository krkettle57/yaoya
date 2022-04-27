from typing import Any, Dict

import pandas as pd


class MemoryStore:
    def __init__(self) -> None:
        self._df = pd.DataFrame()

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    def insert(self, row: Dict[str, Any]) -> None:
        row_df = pd.DataFrame.from_records([row])
        self._df = pd.concat([self._df, row_df])
