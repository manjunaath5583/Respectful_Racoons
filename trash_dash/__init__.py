from typing import Optional

from blessed import Terminal, keyboard
from rich import print
from rich.live import Live

from trash_dash.main_screen import create_screen
from trash_dash.screen import screens

term = Terminal()


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
        current_destroy()
        print("[b]Exiting!")
    except KeyboardInterrupt:
        pass
