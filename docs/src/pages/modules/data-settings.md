---
title: "Storing data and settings"
layout: ../../layouts/Main.astro
---

TrashDash allows modules to store data and define their own settings. These are made possible by the `trash_dash.data` and `trash_dash.settings` modules, respectively.

## Storing data

TrashDash uses [`tinydb`](https://tinydb.readthedocs.io/en/latest/) under-the-hood to manage data, so you'll need to know that if you want to store data.

The `trash_dash.data` module exposes a `Data` class that is a small wrapper around `tinydb`. It will ensure that the data gets stored in the right place.

To use it,

```python
# 1. Import
from trash_dash.data import Data

class HelloWorldModule(Module):
  @classmethod
  def display(cls):
    # 2. Create an object
    data = Data(cls.meta.name)
    # 3. Use data.db to access the tinydb instance.
    data.db.insert({"hello": "world"})
    return "Hello"
```

This can be used to cache data from API requests, like in the [news module](https://github.com/manjunaath5583/respectful_racoons/blob/main/trash_dash/modules/news.py), or store user data, like in the [todo module](https://github.com/manjunaath5583/respectful_racoons/blob/main/trash_dash/modules/todo.py)

## Settings

TrashDash also allows modules to define their own settings. This is powered by the `register` function of the `trash_dash.settings` module.

To use this function,

```python
# 1. Import
from trash_dash.settings import register

class HelloWorldModule(Module):
  @classmethod
  def display(cls):
    # 2. Call the function
    settings = register(cls.meta.name)
    # 3. Use get() or set()
    settings.set("test", "Hello")
    settings.get("test") == "Hello"  # True
    return "Hello"
```

Checkout the [wakatime module](https://github.com/manjunaath5583/respectful_racoons/blob/main/trash_dash/modules/wakatime.py) to see how the `register` function is used.
