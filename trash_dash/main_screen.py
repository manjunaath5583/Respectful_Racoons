"""Main screen"""
from collections.abc import Callable
from typing import Tuple

from rich.align import Align
from rich.columns import Columns
from rich.console import RenderGroup
from rich.padding import Padding

from trash_dash.body import body
from trash_dash.screen import Screen
from trash_dash.settings import get_settings


def create_screen() -> Tuple[Screen, Callable]:
    """Creates and returns a screen"""
    app_settings = get_settings()
    body_renderable, body_destroy = body()
    screen = Screen(
        "main",
        header_renderable=Padding(
            RenderGroup(
                Columns(
                    [
                        Align(
                            f"[bold u]{app_settings.get('app_name', 'TrashDash')}[/]",
                            align="left",
                            vertical="middle",
                        ),
                        Align(
                            "[bold]Settings    Exit(q)[/]",
                            align="right",
                            vertical="middle",
                        ),
                    ],
                    expand=True,
                ),
                Align("Use the [yellow]keyboard[/] to navigate!", align="center"),
            ),
            (1, 3, 0, 3),
        ),
        body_renderable=body_renderable,
    )

    return screen, body_destroy
