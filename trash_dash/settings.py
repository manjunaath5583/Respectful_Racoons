"""Contains methods for manipulating settings.toml"""
import os
from typing import Any

import toml

PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/settings.toml")
)
default_settings = {
    "show_today": True,
    "app_name": "TrashDash",
    "cards": {},
    "modules": {},
}


def _get_settings() -> dict:
    """Gets settings from settings.toml, or creates it if it doesn't exist, or is invalid"""
    if not os.path.exists(PATH):
        with open(PATH, "w") as f:
            toml.dump(default_settings, f)
    # Try reading TOML and see if it is valid
    try:
        with open(PATH, "r") as f:
            return toml.load(f)
    except toml.TomlDecodeError:
        with open(PATH, "w") as f:
            toml.dump(default_settings, f)
    return {}


def _write_settings(data: dict) -> dict:
    with open(PATH, "w") as f:
        toml.dump(data, f)
    return data


class _Settings:
    __name: str

    def __init__(self, name: str):
        """
        An interface for accessing settings of a module

        :param name: Name of the module
        """
        self.__name = name

    @property
    def name(self) -> str:
        """Name of the module"""
        return self.__name

    def get(self, key: str) -> Any:
        """Gets a setting"""
        settings = _get_settings()
        if (
            type(settings.get("module")) != dict
            or type(settings.get("module").get(self.name)) != dict
        ):
            raise Exception("Setting not registered")
        return settings[self.name].get(key)

    def set(self, key: str, value: Any) -> Any:
        """Gets a setting"""
        settings = _get_settings()
        if (
            type(settings.get("module")) != dict
            or type(settings.get("module").get(self.name)) != dict
        ):
            raise Exception("Setting not registered")
        settings[self.name][key] = value
        _write_settings(settings)


def register(name: str):
    """Register a module in settings"""
    settings = _get_settings()
    if type(settings.get("module")) != dict:
        settings["module"] = {}
    if type(settings.get("module").get(name)) != dict:
        settings["module"][name] = {"name": name}
    _write_settings(settings)
    return _Settings(name)
