"""Custom layout class"""

from typing import Dict, Optional

from blessed.keyboard import Keystroke
from rich.console import RenderableType
from rich.layout import Layout

from trash_dash.events import emit

screens: Dict[str, "Screen"] = {}


class Screen:
    name: str
    layout: Layout
    body_layout: Layout
    header_layout: Layout

    def __init__(
        self,
        name: str,
        header_renderable: Optional[RenderableType] = None,
        body_renderable: Optional[RenderableType] = None,
    ):
        """
        Wrapper to create a base layout template. Splits the screen into a header and body.

        :param name: Internal name of the layout
        :param header_renderable: Renderable to be put in the header layout
        :param body_renderable: Renderable to be put in the body layout
        """
        self.name = name
        screens[name] = self

        self.layout = Layout(name=name)
        self.header_layout = Layout(header_renderable, name="header", size=3)
        self.body_layout = Layout(
            body_renderable, name="body", ratio=2, minimum_size=25
        )
        self.layout.split_column(self.header_layout, self.body_layout)

    def render_header(self, item: RenderableType):
        """
        Updates the header layout with the ``item`` renderable

        :param item: The renderable to update the header
        """
        self.header_layout.update(item)

    def render_body(self, item: RenderableType):
        """
        Updates the header layout with the ``item`` renderable

        :param item: The renderable to update the header
        """
        self.body_layout.update(item)

    def keystroke(self, key: Keystroke):
        """Handles key strokes"""
        emit(f"{self.name}.keystroke", key)

    def destroy(self):
        """Handles destroy"""
        emit(f"{self.name}.destroy")
