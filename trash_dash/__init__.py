from typing import Optional

from blessed import Terminal, keyboard
from rich import print
from rich.align import Align
from rich.live import Live
from rich.markup import escape

from trash_dash.cards import cards as _cards
from trash_dash.main_screen import create_screen
from trash_dash.modules import modules
from trash_dash.screen import Screen, screens

term = Terminal()


def _show_more(card_index: int) -> Optional[Screen]:
    try:
        card_item = modules.get(_cards[card_index])
    except IndexError:
        return None
    if not (hasattr(card_item, "display") and bool(card_item.display)):  # type: ignore
        return None
    x = card_item.display()  # type: ignore
    y = card_item.header()
    module_screen = Screen(card_item.meta.name)
    try:
        if not x:
            module_screen.render_header(
                Align(
                    "[b]This module can't be displayed on its own",
                    "center",
                    vertical="middle",
                )
            )
            module_screen.render_body(
                Align("Press ESC to exit", "center", vertical="middle")
            )
            return module_screen
        module_screen.render_header(
            y or Align(f"[b]{escape(card_item.meta.display_name)}")
        )
        module_screen.render_body(x)
        return module_screen
    except (IndexError, TypeError):
        return None


def run():
    """Run the app"""
    current_screen: Optional[Screen] = create_screen()

    try:
        with term.fullscreen(), term.cbreak():
            with Live(screens["main"].layout, screen=True) as live:
                pressed_key: Optional[keyboard.Keystroke] = None
                while pressed_key != "q":
                    pressed_key = term.inkey()
                    if pressed_key.is_sequence and pressed_key.code == 361:
                        # Re-render the main screen when <ESC> is pressed
                        x = create_screen()
                        live.update(x.layout)
                        current_screen = x
                    else:
                        # Pass the keypress to the screen
                        screens["main"].keystroke(pressed_key)
                current_screen.destroy()
        print("[b]Exiting!")
    except KeyboardInterrupt:
        pass
