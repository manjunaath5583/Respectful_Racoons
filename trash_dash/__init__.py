from rich.align import Align
from rich.columns import Columns
from rich.live import Live

from trash_dash.screen import Screen

screen = Screen(
    "main",
    header_renderable=Columns(
        [
            Align("[bold u]TrashDash[/]", align="left", vertical="middle"),
            Align("[bold]Settings[/]", align="right", vertical="middle"),
        ],
        expand=True,
    ),
)


def run():
    """Run the app"""
    try:
        with Live(screen.layout, screen=True):
            while True:
                pass
    except KeyboardInterrupt:
        pass
