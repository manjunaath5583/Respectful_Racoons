"""Weather module"""
from json import JSONDecodeError
from math import floor
from time import time
from typing import Optional, TypedDict

from requests import get
from rich.align import Align
from rich.console import RenderGroup
from rich.padding import Padding
from rich.panel import Panel
from tinydb import Query

from trash_dash.data import Data
from trash_dash.module import Module, register_module
from trash_dash.settings import register


class WeatherLocationType(TypedDict):
    lat: float
    lon: float
    name: str
    region: str
    country: str
    tz_id: str
    localtime: str
    localtime_epoch: str


class WeatherConditionType(TypedDict):
    text: str
    icon: str
    code: int


class WeatherCurrentType(TypedDict):
    last_updated: str
    last_updated_epoch: int
    temp_c: float
    temp_f: float
    feelslike_c: float
    feelslike_f: float
    humidity: int
    cloud: int
    is_day: int
    condition: WeatherConditionType


class WeatherType(TypedDict):
    location: WeatherLocationType
    current: WeatherCurrentType


class WeatherModule(Module):
    @staticmethod
    def get_ip() -> Optional[str]:
        """Gets this computer's public ip"""
        settings = register("weather")
        if settings.get("ip"):
            return settings.get("ip")
        res = get("https://ifconfig.me")
        if res.ok:
            ip = res.content.decode()
            settings.set("ip", ip)
            return ip
        return None

    @classmethod
    def get_weather(cls) -> Optional[WeatherType]:
        """Gets the current weather from the IP"""
        data = Data("weather")
        Q = Query()
        d = data.db.search(
            (Q.cache_time >= (floor(time()) - 86400)) & (Q.cache_time <= floor(time()))
        )
        if d:
            try:
                return d[0].get("weather")
            except (IndexError, KeyError):
                data.db.remove(Q.cache_time - 86400 < floor(time()))
        else:
            data.db.truncate()
        try:
            ip = cls.get_ip()
            if not ip:
                return None
            res = get("https://zh492f.deta.dev/weather?ip=" + ip)
            if not res.ok:
                return None
            weather = res.json()
            data.db.insert(
                {
                    "weather": weather,
                    "cache_time": floor(time()),
                }
            )
            return weather
        except JSONDecodeError:
            return None

    @classmethod
    def today(cls):
        weather = cls.get_weather()
        if not weather:
            return "No weather available"
        return RenderGroup(
            f"[green]{weather['current']['temp_c']}°C[/] - {weather['current']['condition']['text']}",
            Align(
                f"{weather['location']['name']}, {weather['location']['country']}",
                "right",
            ),
        )

    @classmethod
    def card(cls):
        weather = cls.get_weather()
        if not weather:
            return Align("[b]No weather available", "center", vertical="middle")
        current = weather["current"]
        return RenderGroup(
            Padding(
                Align(f"[b]{current['condition']['text']}", "center"), (0, 0, 1, 0)
            ),
            f"[b]Temperature[/b]: [green]{current['temp_c']}°C | {current['temp_f']}°F",
            f"[b]Feels like[/b]: [green]{current['feelslike_c']}°C | {current['feelslike_f']}°F",
            f"[b]Humidity %[/b]: [green]{current['humidity']}%",
            f"[b]Cloud %[/b]: [green]{current['cloud']}%",
            Padding(f"[b]Updated[/b]: [green]{current['last_updated']}", (0, 0, 1, 0)),
        )

    @classmethod
    def header(cls):
        weather = cls.get_weather()
        if not weather:
            return Align("[b]No weather available", "center", vertical="middle")
        location = weather["location"]
        return Padding(
            RenderGroup(
                "[b]Weather",
                f"{location['name']} - {location['country']}",
                f"[b yellow]{weather['current']['condition']['text']}",
            ),
            (0, 2),
        )

    @classmethod
    def display(cls):
        weather = cls.get_weather()
        if not weather:
            return Align("[b]No weather available", "center", vertical="middle")
        current = weather["current"]
        return Panel(
            Padding(
                RenderGroup(
                    f"[b]Weather data",
                    f"[b]Temperature[/b]: [green]{current['temp_c']}°C | {current['temp_f']}°F",
                    f"[b]Feels like[/b]: [green]{current['feelslike_c']}°C | {current['feelslike_f']}°F",
                    f"[b]Humidity %[/b]: [green]{current['humidity']}%",
                    f"[b]Cloud %[/b]: [green]{current['cloud']}%",
                    Padding(
                        f"[b]Updated[/b]: [green]{current['last_updated']}",
                        (0, 0, 1, 0),
                    ),
                    f"Press [b]ESC[/b] to go back to the main menu",
                ),
                (1, 1),
            )
        )


register_module(WeatherModule, "weather", "Weather", "Shows the weather.", True, True)
