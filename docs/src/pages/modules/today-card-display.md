---
title: "The today(), card() and display() methods"
layout: ../../layouts/Main.astro
---

TrashDash allows your module class to expose three methods: `today()`, `card()` and `display()` so that it can be rendered.

Since objects of modules are not created, **these methods should either be a `@staticmethod` or a `@classmethod`**, and if it needs any other methods in the module class, they have to be static too.

## `display()`

Let's take a look at the `display()` method first. The `display()` method allows you to display the method as a screen. The display method must return a `rich.console.RenderableType`, which can be a rich module (like `Align` or `Padding`), or a rich-formatted string.

To get started, add the `display()` method to your module class

```python
from rich.align import Align
from rich.console import RenderableType
# ...
class HelloWorldModule(Module):
  # @classmethod - If you need to access other things from this class
  @staticmethod
  def display() -> RenderableType:
    return Align("[b]Hello, world!", "center", vertical="middle")

# ...
```

Now you can view your module by opening TrashDash, pressing `a`, and then the listed keys to open your module.

### Adding a header

You can notice, that while the body of the module is great, the header looks bland, containing only the `display_name` of the module.

Fear not, for TrashDash allows you to edit the header too!

The concerned method is `header()`, and it works similar to the `display()` module, as in, it should be static, and it should return a `RenderableType`, but instead of modifying the body of the screen, it modifies the header.

Let's add a header to our module.

```python
# ...
class HelloWorldModule(Module):
  # This is a class method because I want to access the display_name and description of this module.
  @classmethod
  def header(cls) -> RenderableType:
    return Align(f"{cls.meta.display_name} - {cls.meta.description}")
  # ...
```

And if you restart TrashDash and look at the module, you'll notice that the header at the top has changed!

## `card()`

The `card()` method allows us to display our module as a card. The `card()` method will only work if you set `allow_card` to `True` when registering your module using the `register_module` function.

The `card()` module is similar to the `display()` function again. It has to be static and return a rich renderable. Let's create a card for our module.

```python
from rich.padding import Padding
# ...
class HelloWorldModule(Module):
  @staticmethod
  def card() -> RenderableType:
    return Padding("Hi!", (1, 2))
  # ...
```

You'll need to add your module's name anywhere in the first three elements of the `cards` array in [`settings.toml`](/settings-toml).

```toml
# trash_dash/data/settings.toml
# ...
cards = ["hello_world", "news", "wakatime"]
# ...
```

And now, you should see your card on the screen!

## `today()`

The `today()` method allows your module to be displayed in the Today card. The `today()` method will only work if you set `allow_today` to `True` when registering your module using the `register_module` function.

> Please return one-liners in the `today()` method. This is so that it doesn't occupy too much space and cause content to go off-screen

We're pretty sure that you can implement this method on your own, so give it a try!

If you get confused, you can always look at the other modules that are built-in to TrashDash.
