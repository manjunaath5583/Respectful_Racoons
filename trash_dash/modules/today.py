"""
This module contains the Today card

The today card MUST NOT be imported in ``__init__.py`` in order to prevent circular import
"""
from typing import List

from rich.console import RenderGroup
from rich.markup import escape
from rich.padding import Padding
from rich.panel import Panel

from trash_dash.module import Module, register_module
from trash_dash.modules import modules


class TodayModule(Module):
    @staticmethod
    def _get_today() -> List[dict]:
        """Generator to get the Today items from each module"""
        to_return = []
        for name, module in modules.items():
            try:
                if module.meta.allow_today:
                    today = module.today()
                    try:
                        destroy_func = today[1]
                    except IndexError:
                        destroy_func = None
                    if today:
                        to_return.append(
                            {
                                "name": name,
                                "renderable": today[0],
                                "destroy_func": destroy_func,
                            }
                        )
            except AttributeError:
                pass
        return to_return

    @classmethod
    def card(cls):
        """Returns the today card"""
        today = TodayModule._get_today()
        items = []
        for i in today:
            items.append(Padding(f"[b u]{escape(i.get('name'))}", (0, 1)))
            items.append(Padding(i.get("renderable"), (0, 4)))

        def destroy():
            for item in today:
                if hasattr(item.get("destroy_func"), "__call__"):
                    item.get("destroy_func")()

        panel = Panel(RenderGroup(*items), title="Today")
        return panel, destroy


register_module(TodayModule, "today", "Today", "Items important today", False, True)
