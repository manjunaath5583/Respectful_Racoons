"""Custom layout class"""

from typing import Optional

from rich.console import RenderableType
from rich.layout import Layout

layouts = {}


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
        layouts[name] = self

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
