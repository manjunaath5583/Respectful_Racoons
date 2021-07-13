"""This file contains the API required to create Modules"""
from collections.abc import Callable
from typing import Optional, Tuple, Union

from rich.console import RenderableType


def register_module(
    module: Union[type, Callable],
    name: str,
    display_name: str,
    description: Optional[str] = None,
    allow_today: bool = False,
    allow_card: bool = False,
):
    """
    Method to create a module. Should be used along with inheriting the ``Module`` class.

    :param module: The module to register
    :param name: The internal name of the module. Name it like you name variables. It'll be used in JSON
    :param display_name: The display name of the module. Shown to users
    :param description: The module's description.
    :param allow_today: Allow this module to appear in the Today card
    :param allow_card: Allow this module to appear in the main screen (when the user wants it to)
    """
    assert issubclass(module, Module)

    module.meta = ModuleMeta(name, display_name, description, allow_today, allow_card)
    if module.meta.allow_today:
        assert hasattr(module, "today")
    if module.meta.allow_card:
        assert hasattr(module, "card")
    assert hasattr(module, "display")
    assert hasattr(module, "header")


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
    """All modules should inherit this class. Should be used with the ``register_module`` function"""

    meta: ModuleMeta

    @staticmethod
    def header() -> Optional[
        Union[Tuple[RenderableType], Tuple[RenderableType, Callable]]
    ]:
        """
        This method is called when the module's header should be displayed, when the module is being displayed.

        :return: It should return a tuple, in which the first item is the Rich renderable, and
        the second item, is optionally a function that'll be called when the module will
        be destroyed.
        """
        pass

    @staticmethod
    def display() -> Optional[
        Union[Tuple[RenderableType], Tuple[RenderableType, Callable]]
    ]:
        """
        This method is called when the module must be displayed in its own screen.

        :return: It should return a tuple, in which the first item is the Rich renderable, and
        the second item, is optionally a function that'll be called when the module will
        be destroyed.
        """
        pass

    @staticmethod
    def today() -> Optional[
        Union[Tuple[RenderableType], Tuple[RenderableType, Callable]]
    ]:
        """
        This method is called when the module must be displayed in the Today card.

        If your module doesn't need a today card, you can return None, (or not implement this method)

        :return: It should return a tuple, in which the first item is the Rich renderable, and
        the second item, is optionally a function that'll be called when the module will
        be destroyed.
        """
        pass

    @staticmethod
    def card() -> Optional[
        Union[Tuple[RenderableType], Tuple[RenderableType, Callable]]
    ]:
        """
        This method is called when the module must be displayed as a card on the main page.

        If your module shouldn't be displayed as a card, you can return None, (or not implement this method)

        :return: It should return a tuple, in which the first item is the Rich renderable, and
        the second item, is optionally a function that'll be called when the module will
        be destroyed.
        """
        pass
