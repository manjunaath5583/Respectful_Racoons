"""Body of the main screen"""
from collections.abc import Callable
from typing import Tuple

from rich.columns import Columns
from rich.console import RenderableType
from rich.padding import Padding

from trash_dash.modules.today import TodayModule


def body() -> Tuple[RenderableType, Callable]:
    """Render the body of the main page"""
    today, today_destroy = TodayModule.card()
    destroy_func = [today_destroy]

    def destroy():
        for i in destroy_func:
            if hasattr(i, "__call__"):
                i()

    return Padding(Columns([today], expand=True), (1, 3)), destroy
