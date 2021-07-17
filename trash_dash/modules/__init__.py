"""Contains a repository of modules"""
from typing import Any, Dict

from trash_dash.modules.example import MyModule
from trash_dash.modules.hacker_news import HackerNewsModule
from trash_dash.modules.news import NewsModule
from trash_dash.modules.wakatime import WakatimeModule
from trash_dash.modules.weather import WeatherModule

# Type: module_name: module_class
modules: Dict[str, Any] = {
    MyModule.meta.name: MyModule,
    HackerNewsModule.meta.name: HackerNewsModule,
    WeatherModule.meta.name: WeatherModule,
    NewsModule.meta.name: NewsModule,
    WakatimeModule.meta.name: WakatimeModule,
}
