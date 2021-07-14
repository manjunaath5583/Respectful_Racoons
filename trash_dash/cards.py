"""The cards on the main screen"""
from collections.abc import Callable
from typing import Tuple

from rich.align import Align
from rich.console import RenderableType, RenderGroup
from rich.panel import Panel

from trash_dash.events import emit
from trash_dash.modules import modules
from trash_dash.settings import get_settings

cards = get_settings().get("cards", [])


def _render_card(card_index: int) -> Tuple[RenderableType, Callable]:
    try:
        name = cards[card_index]
    except IndexError:
        return Align("[b]No card here!", "center", vertical="middle"), lambda: None
    card_item = modules.get(name)
    if not card_item:
        return Align("[b]No card here!", "center", vertical="middle"), lambda: None
    if not card_item.meta.allow_card:
        return Align("[b]No card here!", "center", vertical="middle"), lambda: None
    c = card_item.card()
    if not c:
        return Align("[b]No card here!", "center", vertical="middle"), lambda: None

    def destroy():
        emit(f"{card_item.meta.name}.destroy")

    return (
        Panel(
            RenderGroup(c, f"[i]Press [b]{card_index + 1}[/b] to view"),
            title=card_item.meta.display_name,
        ),
        destroy,
    )


def one():
    """First card - Shown below the Date/Time section"""
    return _render_card(0)


def two() -> Tuple[RenderableType, Callable]:
    """Second card - Shown at the top of the last column"""
    return _render_card(1)


def three() -> Tuple[RenderableType, Callable]:
    """Third card - Shown at the bottom of the last column"""
    return _render_card(2)
