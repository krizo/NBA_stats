from pandas import DataFrame

from data.base_fetcher import BaseFetcher


class PlayersFetcher(BaseFetcher):
    _table_name = "players"

    @classmethod
    def get_by(cls, **kwargs) -> DataFrame:
        query = f"SELECT * FROM Players WHERE "
        params_counter = 0
        for key, value in kwargs.items():
            if params_counter > 0:
                query += " AND "
            query = query + f" {key} = '{value}'"
            params_counter += 1
        return cls._get_dataframe(query)