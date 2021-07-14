from collections.abc import Callable
from typing import Optional, Tuple

from blessed import Terminal, keyboard
from rich import print
from rich.console import RenderableType
from rich.live import Live

from trash_dash.cards import cards as _cards
from trash_dash.main_screen import create_screen
from trash_dash.modules import modules
from trash_dash.screen import screens

term = Terminal()


def _show_more(card_index: int) -> Optional[Tuple[RenderableType, Callable]]:
    try:
        card_item = modules.get(_cards[card_index])
    except IndexError:
        return None
    if not (hasattr(card_item, "display") and bool(card_item.display)):  # type: ignore
        return None
    x = card_item.display()  # type: ignore
    try:
        if not x[0]:
            return None
        if len(x) < 2 or not x[1] or not hasattr(x[1], "__call__"):
            destroy = lambda: None  # noqa: E731
        else:
            destroy = x[1]
        return x[0], destroy
    except (IndexError, TypeError):
        return None


def run():
    """Run the app"""
    current_destroy = create_screen()[1]

    try:
        with term.fullscreen(), term.cbreak():
            with Live(screens["main"].layout, screen=True) as live:
                pressed_key: Optional[keyboard.Keystroke] = None
                while pressed_key != "q":
                    pressed_key = term.inkey()
                    if pressed_key.is_sequence and pressed_key.code == 361:
                        # Re-render the main screen when <ESC> is pressed
                        x, y = create_screen()
                        live.update(x.layout)
                        current_destroy()
                        current_destroy = y
                    else:
                        # Pass the keypress to the screen
                        screens["main"].keystroke_handler(pressed_key)
        current_destroy()
        print("[b]Exiting!")
    except KeyboardInterrupt:
        pass
