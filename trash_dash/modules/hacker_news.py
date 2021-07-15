from json import JSONDecodeError, loads
from math import floor
from time import time

from requests import get
from rich.align import Align
from rich.console import RenderGroup
from rich.markup import escape
from rich.padding import Padding
from rich.text import Text
from tinydb import Query

from trash_dash.data import Data
from trash_dash.module import Module, register_module


class HackerNewsModule(Module):
    @staticmethod
    def get_news():
        """Fetches news from YC"""
        data = Data("hacker_news")
        Q = Query()
        d = data.db.search(
            (Q.cache_time >= (floor(time()) - 86400)) & (Q.cache_time <= floor(time()))
        )
        if d:
            try:
                return d[0].get("stories")
            except (IndexError, KeyError):
                data.db.remove(Q.cache_time - 86400 < floor(time()))
        else:
            data.db.truncate()
        try:
            top_stories_res = get(
                "https://hacker-news.firebaseio.com/v0/topstories.json"
            )
            if not top_stories_res.ok:
                return []
            top_stories: list = loads(top_stories_res.content)
            stories = []
            for index, item in enumerate(top_stories):
                if index > 9:
                    break
                story_res = get(
                    f"https://hacker-news.firebaseio.com/v0/item/{item}.json"
                )
                if not story_res.ok:
                    continue
                story = loads(story_res.content)
                if story["type"] != "story":
                    continue
                stories.append(story)
            data.db.insert(
                {
                    "top_stories": top_stories,
                    "stories": stories,
                    "cache_time": floor(time()),
                }
            )
            return stories
        except JSONDecodeError:
            return []

    @classmethod
    def card(cls):
        """Card"""
        news = cls.get_news()
        try:
            news = news[0:5]
        except IndexError:
            return Padding("[b]No news today!", (1, 3))
        news_renders = list(
            map(
                lambda x: RenderGroup(
                    Text(f"{escape(x['by'])}", style="bold"),
                    Text(f"  {escape(x['title'])}", overflow="ellipsis"),
                ),
                news,
            )
        )
        return RenderGroup(
            "[b u]Top posts:", Padding(RenderGroup(*news_renders), (1, 2))
        )

    @classmethod
    def today(cls):
        """Today"""
        news = cls.get_news()
        try:
            x = news[0]
        except IndexError:
            return Padding("[b]No news today!", (1, 3))
        return RenderGroup(
            Text(f"{escape(x['by'])}", style="bold"),
            Text(f"  {escape(x['title'])}", overflow="ellipsis"),
        )

    @classmethod
    def display(cls):
        """Display"""
        news = cls.get_news()
        if not news:
            return Padding("[b]No news today!", (1, 3))
        news_renders = list(
            map(
                lambda x: RenderGroup(
                    Text(f"{escape(x['by'])}", style="bold"),
                    Text(f"  {escape(x['title'])}", overflow="ellipsis"),
                    f"  {x['url']}",
                ),
                news,
            )
        )
        return RenderGroup(
            "[b u]Top posts:", Padding(RenderGroup(*news_renders), (1, 2))
        )

    @staticmethod
    def header():
        """Header"""
        return Align("[b]HackerNews", "center", vertical="middle")


register_module(
    HackerNewsModule, "hacker_news", "Hacker News", "Fetches YC Hacker news", True, True
)
