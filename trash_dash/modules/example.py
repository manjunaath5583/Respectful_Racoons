from rich.align import Align

# Import the module API
from trash_dash.module import Module, register_module


class MyModule(Module):
    @classmethod
    def header(cls):
        """
        This method should return a Rich renderable

        It will be displayed in the header of the module's screen
        """
        return Align(
            f"{cls.meta.display_name} - {cls.meta.description}",
            align="center",
            vertical="middle",
        )

    @staticmethod
    def display():
        """
        This method should return a Rich renderable.

        That can be a rich formatted string, or any other Rich renderable.
        Checkout the Rich Docs for more.
        """
        # This string will be bold
        return "[b]My first module!"


register_module(
    module=MyModule,
    name="example_module",
    display_name="An example",
    description="Just an example!",
    # If the module can be displayed in the Today card
    allow_today=True,
    # If the module can be displayed as a card on the main screen
    allow_card=True,
)
