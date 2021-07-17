"""Contains a repository of modules"""
from typing import Any, Dict

from trash_dash.modules.example import MyModule
from trash_dash.modules.hacker_news import HackerNewsModule
from trash_dash.modules.weather import WeatherModule

# Type: module_name: module_class
modules: Dict[str, Any] = {
    MyModule.meta.name: MyModule,
    HackerNewsModule.meta.name: HackerNewsModule,
    WeatherModule.meta.name: WeatherModule,
}
