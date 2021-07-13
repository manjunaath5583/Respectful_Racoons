from typing import Optional

from blessed import Terminal, keyboard
from rich import print
from rich.align import Align
from rich.columns import Columns
from rich.console import RenderGroup
from rich.live import Live
from rich.padding import Padding

from trash_dash.body import body
from trash_dash.screen import Screen
from trash_dash.settings import get_settings

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
                        "[bold]Settings    Exit(q)[/]", align="right", vertical="middle"
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

term = Terminal()


def run():
    """Run the app"""
    try:
        with term.fullscreen(), term.cbreak():
            with Live(screen.layout, screen=True):
                pressed_key: Optional[keyboard.Keystroke] = None
                while pressed_key != "q":
                    pressed_key = term.inkey()
        body_destroy()
        print("[b]Exiting!")
    except KeyboardInterrupt:
        pass
