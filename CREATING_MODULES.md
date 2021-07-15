# Creating custom modules

Weather its for your own setup, or to contribute to us (thank you!), you can create custom modules in TrashDash.

## Prerequisites
- Python 3.9 with Poetry installed
- Python knowledge
- Knowledge of the Rich Framework

## The module API

TrashDash uses an event-driven module API. All you have to do is define your module and listen to events. Everything else is done by TrashDash.

To get started, create a python file in `trash_dash/modules`. This file should be named like how you name variables in python.

Here are some examples of valid and invalid names:
**Valid**:
- `weather.py`
- `multiple_words.py`
- `my_custom_module12.py`

**Invalid**:
- `Hello world.py`
- `my-module.py`
- `#$)(!()#.py`

## Your module

Open the file you just created in your favorite python editor, and let's start coding!

First, import the module API
```python
from trash_dash.module import register_module, Module
```

Next, create a module class
```python
class MyModule(Module):
    pass
```

Register your module right under where you defined the class.
```python
register_module(
  module=MyModule,
  name="example_module",
  display_name="An example",
  description="Just an example!",
  # If the module can be displayed in the Today card
  allow_today=True,
  # If the module can be displayed as a card on the main screen
  allow_card=True
)
```

And finally, you'll need to add your module to `trash_dash/modules/__init__.py` so that TrashDash knows about it.

Import your module class above, and add your module to the `modules` dict following the other modules. Be sure NOT to delete any modules!

If you've done everything right, this is how `__init__.py` should look like:

```python
"""Contains a repository of modules"""
from typing import Any, Dict

from trash_dash.modules.hacker_news import HackerNewsModule
from trash_dash.modules.example import MyModule

# Type: module_name: module_class
modules: Dict[str, Any] = {
  HackerNewsModule.meta.name: HackerNewsModule,
  MyModule.meta.name: MyModule,
}
```

Checkout the [example module](https://github.com/manjunaath5583/respectful_racoons/tree/main/trash_dash/modules/example.py) if you get confused.

## Displaying data

Modules can display data when they're viewed. To display data, you have to return a rich renderable in the `display` method of your module.

Here's an example:

```python
class MyModule(Module):
  @staticmethod
  def display():
    """
    This method should return a Rich renderable.

    That can be a rich formatted string, or any other Rich renderable.
    Checkout the Rich Docs for more.
    """

    # This string will be bold
    return "[b]My first module!"
```

> Make sure that `display` is either a `@staticmethod` or a `@classmethod`

Now you can view your module! Run the app with `poetry run python3 main.py`, and press `a` to view all modules.
You should see your module listed there! Press the keystrokes on your screen to get to it, and you will see whatever you've returned in `display` on your screen!

## Header

Notice how our header looks really bland. It just shows the display name of our module. We can easily change the header, just like the display, using the `header` method.

Just like the `display` method, the `header` method of your module's class should be a `@staticmethod` or a `@classmethod` that returns a Rich renderable.

Example:
```python
class MyModule(Module):
  @classmethod
  def header(cls):
    """
    This method should return a Rich renderable

    It will be displayed in the header of the module's screen
    """
    return Align(f"{cls.meta.display_name} - {cls.meta.description}", align="center", vertical="middle")
```

> Remember to import the `Align` class from `rich.align`.

Now if you view your card, you'll see a centered header on the screen.

## Cards

TBD

## Today

TBD

## Listening to events

TrashDash emits and listens to certain events in your modules. These events are:

All events will be prefixed with your module's name and a period (`.`).
**Emitted**:
- `event_loop` - Emitted every second. This event can be used to update the screen.
- `keystroke` - Emitted when a keystroke is received.
- `destroy` - Emitted when the module has been removed from the screen. Use this event to store data, close files, etc.

**Listened to**:
- `update` - When this event is emitted, along with a renderable, the renderable will be rendered on the screen.

How to listen to/emit events:

Import the necessary method from `trashdash.events`

```python3
from trash_dash.events import on, emit, once, off

# Listens to the event_loop event in your module
on("mymodule.event_loop", function)

# Listens to the destroy event in your module ONLY ONCE
once("mymodule.destroy", function)

# Emits the update event of your module
emit("mymodule.update", optional_data)

# Stops listening to the keystroke event of your module
off("mymodule.keystroke")
```

## Contributing modules

If you want to contribute a module (thank you!), you have to follow some guidelines.

- Do run `poetry run precommit install` to install precommit hooks.
- Add the module file and edit `trash_dash/modules/__init__.py` ONLY. Don't make any other changes, except, installing other packages.
- Be sure to format and lint your code before PR-ing.
- The branch should be named `add-module-modulename`, if `modulename` is the name of your module.
- The PR should be named `Add module modulename`, if `modulename` is the name of your module.

Thank you for contributing!
