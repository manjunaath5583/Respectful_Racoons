import os
import platform
from typing import Optional

from blessed import Terminal, keyboard
from rich import print
from rich.align import Align
from rich.live import Live
from rich.markup import escape

from trash_dash.all_modules import all_modules
from trash_dash.body import console
from trash_dash.cards import cards as _cards
from trash_dash.events import off, on
from trash_dash.main_screen import create_screen
from trash_dash.modules import modules
from trash_dash.screen import Screen, screens

term = Terminal()


def _show_more(card_index: int) -> Optional[Screen]:
    try:
        card_item = modules.get(_cards[card_index])
    except IndexError:
        return None
    if not card_item:
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


current_screen: Screen = create_screen()


def run():
    """Run the app"""
    global current_screen

    if console.height < 25 or console.width <= 100:
        print("[red b]The console window is too small for the app to run!")
        return

    try:
        with term.fullscreen(), term.cbreak():
            with Live(screens["main"].layout, console=console, screen=True) as live:
                pressed_key: Optional[keyboard.Keystroke] = None

                def render_module(module_name: str):
                    global current_screen
                    module = modules.get(module_name)
                    if not module:
                        return
                    body = module.display()
                    head = module.header()
                    module_screen = Screen(module.meta.name, header_renderable=head)
                    if not body:
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
                        live.update(module_screen.layout)
                        off(f"{current_screen.name}.update")
                        current_screen.destroy()
                        current_screen = module_screen
                        on(f"{current_screen.name}.update", live.update)
                        return
                    module_screen.render_header(
                        head or Align(f"[b]{escape(module.meta.display_name)}")
                    )
                    module_screen.render_body(body)
                    live.update(module_screen.layout)
                    current_screen.destroy()
                    current_screen = module_screen

                on(f"{current_screen.name}.update", live.update)
                on("render_module", render_module)

                while pressed_key != "q":
                    current_screen.event_loop()
                    pressed_key = term.inkey(timeout=1)
                    if pressed_key.is_sequence and pressed_key.code == 361:
                        # Re-render the main screen when <ESC> is pressed
                        x = create_screen()
                        live.update(x.layout)
                        current_screen.destroy()
                        current_screen = x
                    elif pressed_key == "s":
                        start_keyword = "start"
                        if platform.system().lower() == "linux":
                            start_keyword = "xdg-open"
                        elif platform.system().lower() == "darwin":
                            start_keyword = "open"
                        os.system(  # noqa: S605
                            start_keyword
                            + " "
                            + os.path.abspath(
                                os.path.join(
                                    os.path.dirname(os.path.abspath(__file__)),
                                    "data/settings.toml",
                                )
                            )
                        )
                    elif current_screen.name == "main" and pressed_key in [
                        "1",
                        "2",
                        "3",
                    ]:
                        card_index = int(pressed_key) - 1
                        mod = _show_more(card_index)
                        if mod:
                            live.update(mod.layout)
                            current_screen.destroy()
                            current_screen = mod
                    elif pressed_key == "a":
                        x = all_modules()
                        live.update(x.layout)
                        current_screen.destroy()
                        current_screen = x
                    else:
                        # Pass the keypress to the screen
                        current_screen.keystroke(pressed_key)
                off(f"{current_screen.name}.update")
                current_screen.destroy()
        print("[b]Exiting!")
    except KeyboardInterrupt:
        pass
