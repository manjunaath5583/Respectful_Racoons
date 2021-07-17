"""Module that shows wakatime stats"""
from math import floor
from time import time
from typing import List, Optional, TypedDict

from requests import get
from rich.align import Align
from rich.columns import Columns
from rich.console import RenderableType, RenderGroup
from rich.padding import Padding
from rich.panel import Panel
from tinydb import Query

from trash_dash.data import Data
from trash_dash.module import Module, register_module
from trash_dash.settings import register


class WakatimeItemType(TypedDict):
    digital: str
    hours: int
    minutes: int
    name: str
    percent: str
    text: str
    total_seconds: float


class WakatimeStatsType(TypedDict):
    human_readable_daily_average: str
    human_readable_total: str
    editors: List[WakatimeItemType]
    languages: List[WakatimeItemType]


class WakatimeResponseType(TypedDict):
    data: WakatimeStatsType


class WakatimeModule(Module):
    @staticmethod
    def get_wakatime_stats() -> Optional[WakatimeStatsType]:
        """Gets the wakatime statistics"""
        settings = register("wakatime")
        data = Data("wakatime")
        Q = Query()
        d = data.db.search(
            (Q.cache_time >= (floor(time()) - 86400)) & (Q.cache_time <= floor(time()))
        )
        if d:
            try:
                return d[0].get("wakatime")
            except (IndexError, KeyError):
                data.db.remove(Q.cache_time - 86400 < floor(time()))
        else:
            data.db.truncate()
        if (
            not settings.get("username")
            or settings.get("username") == "ENTER YOUR WAKATIME USERNAME"
        ):
            settings.set("username", "ENTER YOUR WAKATIME USERNAME")
            return None
        res = get(
            f"https://wakatime.com/api/v1/users/{settings.get('username')}/stats/last_7_days"
        )
        if not res.ok:
            return {}
        wakatime: WakatimeResponseType = res.json()
        data.db.insert({"cache_time": floor(time()), "wakatime": wakatime.get("data")})
        return wakatime.get("data")

    @classmethod
    def today(cls):
        stats = cls.get_wakatime_stats()
        if stats is None:
            return "[i]Wakatime username is not set in settings!"
        if type(stats) == dict and not stats:
            # If stats is an empty dict
            return "[i]No stats to be displayed"
        return f"[b green]{stats['human_readable_total']}[/] coded this week!"

    @classmethod
    def header(cls):
        return Align("[b]Wakatime", "center", vertical="middle")

    @classmethod
    def card(cls):
        stats = cls.get_wakatime_stats()
        if stats is None:
            return Align(
                "[i]Wakatime username is not set in settings!",
                "center",
                vertical="middle",
            )
        if type(stats) == dict and not stats:
            # If stats is an empty dict
            return Align("[i]No stats to be displayed", "center", vertical="middle")
        return RenderGroup(
            f"[b green]{stats['human_readable_total']}[/] coded this week!\n"
            f"with a [b green]{stats['human_readable_daily_average']}[/] daily average!"
            "\n",
            f"[b]Most used editor[/b]: [aqua]{stats['editors'][0]['name']}[/]",
            f"  with [b green]{stats['editors'][0]['text']}[/] usage this week" "\n",
            f"[b]Most used language[/b]: [aqua]{stats['languages'][0]['name']}[/]",
            f"  with [b green]{stats['languages'][0]['text']}[/] usage this week",
        )

    @classmethod
    def display(cls):
        stats = cls.get_wakatime_stats()
        if stats is None:
            return Align(
                "[i]Wakatime username is not set in settings!",
                "center",
                vertical="middle",
            )
        if type(stats) == dict and not stats:
            # If stats is an empty dict
            return Align("[i]No stats to be displayed", "center", vertical="middle")
        editor_render: List[RenderableType] = []
        for index, editor in enumerate(stats["editors"]):
            editor_render.append(
                RenderGroup(
                    f"[b]{index + 1}. {editor['name']}", f"  {editor['text']} this week"
                )
            )
        language_render: List[RenderableType] = []
        for index, lang in enumerate(stats["editors"]):
            lang: WakatimeItemType = lang  # manually type-cast
            language_render.append(
                RenderGroup(
                    f"[b]{index + 1}. {lang['name']}", f"  {lang['text']} this week"
                )
            )
        return Padding(
            RenderGroup(
                f"[b green]{stats['human_readable_total']}[/] coded this week!\n"
                f"with a [b green]{stats['human_readable_daily_average']}[/] daily average!"
                "\n",
                f"[b]Most used editor[/b]: [aqua]{stats['editors'][0]['name']}[/]",
                f"  with [b green]{stats['editors'][0]['text']}[/] usage this week"
                "\n",
                f"[b]Most used language[/b]: [aqua]{stats['languages'][0]['name']}[/]",
                f"  with [b green]{stats['languages'][0]['text']}[/] usage this week",
                Padding(
                    Columns(
                        [
                            Panel(RenderGroup(*editor_render), title="Editors"),
                            Panel(RenderGroup(*language_render), title="Languages"),
                        ],
                        equal=True,
                    ),
                    (1, 2),
                ),
            ),
            (1, 3),
        )


register_module(
    WakatimeModule, "wakatime", "Wakatime", "Shows your Wakatime statistics", True, True
)
