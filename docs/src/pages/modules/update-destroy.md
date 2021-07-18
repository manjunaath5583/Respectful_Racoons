---
title: "Handling updates and destroys"
layout: ../../layouts/Main.astro
---

TrashDash allows your module to update itself every second, and run code when it gets destroyed (removed from the screen).

## Updating

Let's look at updates first. TrashDash emits the `module_name.event_loop` method every second. This allows your module to update itself by emitting the `module_name.update` method.

Updates are only possible when the module is displayed on its own screen, and only work on the body.

Updating is done in two steps:

1. Listen to the `module_name.event_loop` event.

```python
# ...
class HelloWorldModule(Module):
  @classmethod
  def display(cls):
    def update_handler():
      # called every second
      pass

    on(f"{cls.meta.name}.event_loop", update_handler)

    return "test"
  # ...
```

2. Call the `module_name.update` event

```python
# ...
class HelloWorldModule(Module):
  @classmethod
  def display(cls):
    def update_handler():
      # called every second
      emit(f"{cls.meta.name}.update", "[b] test") # The second argument should be a rich renderable that'll replace the body

    on(f"{cls.meta.name}.event_loop", update_handler)

    return "test"
  # ...
```

And that's how easy it is to automatically update your application every second.

### Manually updating

You can also emit the `module_name.update` event on its own, say when a user [presses a key](/modules/keystrokes). This is called manual updating.

## Destroy

TrashDash also allows your module to run code when it gets removed from the screen (destroyed). This can be used to close database connections, sync data, change settings, etc.

This is similar to the update event, but instead of using `on`, you should use `once`, since the module can only get destroyed once. Also, the `module_name.destroy` is called even when your module gets removed from Today or from the main screen (as a card).

Here's an example.

```python
from trash_dash.events import once

class HelloWorldModule(Module):
  @classmethod
  def card(cls):
    def destroy():
      print("Module was destroyed!")
    once(f"{cls.meta.name}.destroy", destroy)

    return "test"
```
