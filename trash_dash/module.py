"""This file contains the API required to create Modules"""
from collections.abc import Callable
from functools import wraps
from typing import Optional, Tuple, Union

from rich.console import RenderableType


def module(
    name: str,
    display_name: str,
    description: Optional[str] = None,
    allow_today: bool = False,
    allow_card: bool = False,
):
    """
    Decorator to create a module. Should be used along with inheriting the ``Module`` class.

    :param name: The internal name of the module. Name it like you name variables. It'll be used in JSON
    :param display_name: The display name of the module. Shown to users
    :param description: The module's description.
    :param allow_today: Allow this module to appear in the Today card
    :param allow_card: Allow this module to appear in the main screen (when the user wants it to)
    """

    def decorate(cls: Callable):
        @wraps(cls)
        def wrapper(*args, **kwargs):
            obj = cls(*args, **kwargs)
            assert isinstance(obj, Module)

            obj.meta = ModuleMeta(
                name, display_name, description, allow_today, allow_card
            )
            if obj.meta.allow_today:
                assert hasattr(obj, "today")
            if obj.meta.allow_card:
                assert hasattr(obj, "card")
            assert hasattr(obj, "display")

            return obj

        return wrapper

    return decorate


class ModuleMeta:
    def __init__(
        self,
        name: str,
        display_name: str,
        description: Optional[str] = None,
        allow_today: bool = False,
        allow_card: bool = False,
    ):
        self.__name = name
        self.__display_name = display_name
        self.__description = description
        self.__allow_today = allow_today
        self.__allow_card = allow_card

    @property
    def name(self):
        """Internal name of the module"""
        return self.__name

    @property
    def display_name(self):
        """Name of the module shown to users"""
        return self.__display_name

    @property
    def description(self):
        """Module's description"""
        return self.__description

    @property
    def allow_today(self):
        """If the module is allowed to be in the Today card"""
        return self.__allow_today

    @property
    def allow_card(self):
        """If the module is allowed to be displayed as a card"""
        return self.__allow_card


class Module:
    """All modules should inherit this class. Should be used with the ``module`` decorator"""

    meta: ModuleMeta

    def display(
        self,
    ) -> Optional[Union[Tuple[RenderableType], Tuple[RenderableType, Callable]]]:
        """
        This method is called when the module must be displayed in its own screen.

        :return: It should return a tuple, in which the first item is the Rich renderable, and
        the second item, is optionally a function that'll be called when the module will
        be destroyed.
        """
        pass

    def today(
        self,
    ) -> Optional[Union[Tuple[RenderableType], Tuple[RenderableType, Callable]]]:
        """
        This method is called when the module must be displayed in the Today card.

        If your module doesn't need a today card, you can return None, (or not implement this method)

        :return: It should return a tuple, in which the first item is the Rich renderable, and
        the second item, is optionally a function that'll be called when the module will
        be destroyed.
        """
        pass

    def card(
        self,
    ) -> Optional[Union[Tuple[RenderableType], Tuple[RenderableType, Callable]]]:
        """
        This method is called when the module must be displayed as a card on the main page.

        If your module shouldn't be displayed as a card, you can return None, (or not implement this method)

        :return: It should return a tuple, in which the first item is the Rich renderable, and
        the second item, is optionally a function that'll be called when the module will
        be destroyed.
        """
        pass
