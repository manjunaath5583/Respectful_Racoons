"""The date and time that is shown on the main screen"""
from datetime import datetime

from rich.align import Align
from rich.console import RenderableType, RenderGroup
from rich.padding import Padding


def date_time_section() -> RenderableType:
    """Returns the datetime display"""
    now = datetime.now()
    return Padding(
        RenderGroup(
            Align(f"[b green]{now.strftime('%d %b %Y')}", "center"),
            Align(f"[b lime]{now.strftime('%I:%M %p')}", "center"),
        ),
        (1, 2),
    )
