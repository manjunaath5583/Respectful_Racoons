from json import JSONDecodeError
from math import floor
from time import time
from typing import Optional, TypedDict

from requests import get
from tinydb import Query

from trash_dash.data import Data
from trash_dash.module import Module, register_module


class Covid19Type(TypedDict):
    population: int
    deaths: int
    recovered: int
    confirmed: int


class CovidModule(Module):
    @classmethod
    def get_data(cls) -> Optional[Covid19Type]:
        """Gets the latest worldwide news"""
        data = Data("covid")
        Q = Query()
        d = data.db.search(
            (Q.cache_time >= (floor(time()) - 86400)) & (Q.cache_time <= floor(time()))
        )
        if d:
            try:
                return d[0].get("covid")
            except (IndexError, KeyError):
                data.db.remove(Q.cache_time - 86400 < floor(time()))
        else:
            data.db.truncate()
        try:
            res = get("https://covid-api.mmediagroup.fr/v1/cases")
            if not res.ok:
                return None
            covid = res.json().get("Global").get("All")
            data.db.insert(
                {
                    "covid": covid,
                    "cache_time": floor(time()),
                }
            )
            return covid
        except JSONDecodeError:
            return None

    @classmethod
    def today(cls):
        covid = cls.get_data()
        if not covid:
            return "No data available"
        return f"[green b]{covid['confirmed']}[/] cases till now"


register_module(
    CovidModule, "covid", "Covid 19 Data", "Displays covid19 cases", True, True
)
