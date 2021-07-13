"""The cards on the main screen"""
from collections.abc import Callable
from typing import Tuple

from rich.align import Align
from rich.console import RenderableType

from trash_dash.modules import modules
from trash_dash.settings import get_settings

cards = get_settings().get("cards", [])


def _render_card(card_index: int) -> Tuple[RenderableType, Callable]:
    try:
        card_item = modules.get(cards[card_index])
    except IndexError:
        card_item = None
    if not card_item:
        return Align("[b]No card here!", "center", vertical="middle"), lambda: None
    c = card_item.card()
    if not c or not c[0]:
        return Align("[b]No card here!", "center", vertical="middle"), lambda: None
    try:
        destroy = c[1]
    except IndexError:
        destroy = lambda: None  # noqa: E731
    return c[0], destroy


def one():
    """First card - Shown below the Date/Time section"""
    return _render_card(0)


def two() -> Tuple[RenderableType, Callable]:
    """Second card - Shown at the top of the last column"""
    return _render_card(1)


def three() -> Tuple[RenderableType, Callable]:
    """Third card - Shown at the bottom of the last column"""
    return _render_card(2)
