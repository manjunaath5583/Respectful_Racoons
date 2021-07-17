"""News module"""
from json import JSONDecodeError
from math import floor
from time import time
from typing import List, Optional, TypedDict

from requests import get
from rich.align import Align
from rich.console import RenderGroup
from tinydb import Query

from trash_dash.data import Data
from trash_dash.module import Module, register_module


class NewsType(TypedDict):
    title: str
    description: str
    content: str
    url: str


class NewsModule(Module):
    @classmethod
    def get_news(cls) -> Optional[List[NewsType]]:
        """Gets the latest worldwide news"""
        data = Data("news")
        Q = Query()
        d = data.db.search(
            (Q.cache_time >= (floor(time()) - 86400)) & (Q.cache_time <= floor(time()))
        )
        if d:
            try:
                return d[0].get("news")
            except (IndexError, KeyError):
                data.db.remove(Q.cache_time - 86400 < floor(time()))
        else:
            data.db.truncate()
        try:
            res = get("https://zh492f.deta.dev/news")
            if not res.ok:
                return None
            news = res.json().get("articles")
            data.db.insert(
                {
                    "news": news,
                    "cache_time": floor(time()),
                }
            )
            return news
        except JSONDecodeError:
            return None

    @classmethod
    def today(cls):
        news = cls.get_news()
        if not news:
            return "No news available"
        news = news[0:2]
        return RenderGroup(news[0]["title"])

    @classmethod
    def card(cls):
        news = cls.get_news()
        if not news:
            return "No news available"
        news = news[0:3]
        return RenderGroup(
            *list(map(lambda x: f"[b]{news.index(x) + 1}. {x['title']}", news))
        )

    @classmethod
    def header(cls):
        return Align("[b]News", "center", vertical="middle")

    @classmethod
    def display(cls):
        news = cls.get_news()
        if not news:
            return "No news available"
        news = news[0:5]
        return RenderGroup(
            *list(
                map(
                    lambda x: RenderGroup(
                        f"[b]{news.index(x) + 1}. {x['title']}",
                        x["description"],
                        x["url"],
                        "---",
                    ),
                    news,
                )
            )
        )


register_module(NewsModule, "news", "News", "Shows the latest news.", True, True)
