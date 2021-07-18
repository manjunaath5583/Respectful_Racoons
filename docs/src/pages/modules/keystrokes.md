---
title: "Listening to Keystrokes"
layout: ../../layouts/Main.astro
---

TrashDash allows you to listen to keystrokes using its [event api](https://github.com/manjunaath5583/respectful_racoons/blob/main/trash_dash/events.py).

The event api exposes four important methods:

- `on("event_name", handler)` - Executes the `handler` function whenever the `event_name` event is emitted.
- `off("event_name")` - Stops listening to the `event_name` event.
- `once("event_name", handler)` - Executes `handler` when the `event_name` event is emitted, but only does it once.
- `emit("event_name", *args)` - Emits `event_name` and passes `*args` to the handler.

TrashDash emits and listens to a couple of events. Replace `module_name` with the name of your module in the below list.
**Emitted**:

- `module_name.event_loop` - Emitted every second. This event can be used to update the screen.
- `module_name.keystroke` - Emitted when a keystroke is received.
- `module_name.destroy` - Emitted when the module has been removed from the screen. Use this event to store data, close files, etc.

**Listened to**:

- `module_name.update` - When this event is emitted, along with a renderable, the renderable will be rendered on the screen.
- `seize_keystrokes` - Allows the module to [seize keystrokes](/modules/keystrokes#seizing-keystrokes)

## Getting started

We'll be listening to the `module_name.keystrokes` event to handle keystrokes.

Let's make it so that whenever the user presses `d`, it'll add the current time to the `settings.toml` file. For more information on module-specific settings, click [here](/modules/data-settings).

```python
from time import time

from blessed.keyboard import Keystroke

from trash_dash.events import on
from trash_dash.settings import register
# ...

class HelloWorldModule(Module):
  @classmethod
  def display(cls) -> RenderableType:
    settings = register(cls.meta.name) # Get the settings for the current module
    def handler(key: Keystroke):
      if key == "d":
        settings.set("time", time())
      on(f"{cls.meta.name}.keystroke", handler)

      return "Press [b]d[/]!"
# ...
```

And that is how easy it is to listen to keystrokes. For more information about the `Keystroke` type, read the [`blessed` documentation](https://blessed.readthedocs.io/en/latest/keyboard.html).

## Seizing keystrokes

Some keystrokes don't get emitted to the module, and instead, do their respective function.

TrashDash allows a module to seize keystrokes, meaning, it makes TrashDash send **every** keystroke (except `ESC`) to the module. This will prevent the user from viewing all modules, opening settings and exiting TrashDash when the keystrokes are seized. This should obviously be used responsibly.

To seize keystrokes, emit the `seize_keystroke` event with `True` to seize, and `False` to stop seizing.

```python
# ...
  @staticmethod
  def display():
    if key == "q":
      # Stop seizing
      emit("seize_keystokes", False)

    emit("seize_keystrokes", True)  # True isn't required, it is default
    # Now `handler` will receive all keystrokes, including `q`, `a` and `s`
    on(f"{cls.meta.name}.keystroke", handler)

    return "Press [b]d[/]!"
# ...
```
