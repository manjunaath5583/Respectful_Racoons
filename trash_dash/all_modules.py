from typing import List

from blessed.keyboard import Keystroke
from rich.align import Align
from rich.console import RenderableType, RenderGroup
from rich.markup import escape
from rich.padding import Padding

from trash_dash.events import emit, on
from trash_dash.modules import modules
from trash_dash.screen import Screen

keys = ""
modules_list = list(modules.values())


def all_modules() -> Screen:
    """Renders the ``all modules`` screen"""
    global modules_list
    s = Screen(
        "all_modules",
        header_renderable=Padding(
            Align("[b]All modules", "center", vertical="middle"), (1, 3)
        ),
    )
    renders: List[RenderableType] = []

    for index, i in enumerate(modules_list):
        renders.append(
            RenderGroup(
                f"[b]{escape(i.meta.display_name)}[/b] - {escape(i.meta.description or 'No description provided')}",
                Padding(f"[i]Press [/i]{index + 1} and ENTER[i] to open"),
            )
        )

    def handle_keystroke(key: Keystroke):
        global keys, modules_list
        if not key.is_sequence:
            if key.isnumeric():
                keys += key
        elif key.name == "KEY_ENTER":
            if keys.isnumeric():
                try:
                    if modules_list[int(keys) - 1]:
                        emit("render_module", modules_list[int(keys) - 1].meta.name)
                        return
                except (IndexError, TypeError):
                    pass
            keys = ""

    on("all_modules.keystroke", handle_keystroke)

    s.render_body(Padding(RenderGroup(*renders), (1, 3)))

    return s
