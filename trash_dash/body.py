"""Body of the main screen"""
from collections.abc import Callable
from typing import Tuple

from rich.align import Align
from rich.columns import Columns
from rich.console import RenderableType, RenderGroup
from rich.padding import Padding

from trash_dash import cards
from trash_dash.console import console
from trash_dash.date_time_section import date_time_section
from trash_dash.events import emit
from trash_dash.modules.today import TodayModule


def body() -> Tuple[RenderableType, Callable, Callable]:
    """Render the body of the main page"""
    today = TodayModule.card()
    one, destroy_one = cards.one()
    two, destroy_two = cards.two()
    three, destroy_three = cards.three()

    def destroy():
        emit("today.destroy")
        destroy_one()
        destroy_two()
        destroy_three()

    def update():
        return RenderGroup(
            Align("Press [b]a[/b] to view all modules", "center"),
            Align("Press [b]ESC[/b] to return back to the main screen", "center"),
            Padding(
                Columns(
                    [
                        today,
                        RenderGroup(date_time_section(), Padding(one, (2, 0))),
                        RenderGroup(two, Padding(three, (2, 0))),
                    ],
                    width=(console.width // 3) - 3,
                ),
                (1, 3),
            ),
        )

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
                    width=(console.width // 3) - 3,
                ),
                (1, 3),
            ),
        ),
        destroy,
        update,
    )
