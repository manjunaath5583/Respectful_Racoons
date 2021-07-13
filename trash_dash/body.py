"""Body of the main screen"""
from collections.abc import Callable
from typing import Tuple

from rich.align import Align
from rich.columns import Columns
from rich.console import RenderableType, RenderGroup
from rich.padding import Padding

from trash_dash import cards
from trash_dash.date_time_section import date_time_section
from trash_dash.modules.today import TodayModule


def body() -> Tuple[RenderableType, Callable]:
    """Render the body of the main page"""
    today, today_destroy = TodayModule.card()
    destroy_func = [today_destroy]
    one, destroy_one = cards.one()
    two, destroy_two = cards.two()
    three, destroy_three = cards.three()

    def destroy():
        for i in destroy_func:
            if hasattr(i, "__call__"):
                i()
        destroy_one()
        destroy_two()
        destroy_three()

    return (
        RenderGroup(
            Align("Press [b]a[/b] to view all modules", "center"),
            Padding(
                Columns(
                    [
                        today,
                        RenderGroup(date_time_section(), Padding(one, (2, 0))),
                        RenderGroup(two, Padding(three, (2, 0))),
                    ],
                    expand=True,
                ),
                (1, 3),
            ),
        ),
        destroy,
    )
