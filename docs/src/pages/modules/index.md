---
title: "Custom modules"
layout: ../../layouts/Main.astro
---

TrashDash allows you to define custom modules using its Module API.

## Prerequisites

- Python knowledge
- Knowledge of the `rich` library
- **OPTIONAL:** Knowledge of the `requests` library if you want to make API requests
- **OPTIONAL:** Knowledge of the `tinydb` library if you want to store data

## Get started

To create a new module, create a python file in `trash_dash/modules`. Make sure that the file is named how you name variables.

For this tutorial, I'll go with the name `hello_world.py`.

Add the below code to the file

```python
# Import the Module API
from trash_dash.module import Module, register_module


class HelloWorldModule(Module):
    pass


register_module(
    # The module class
    module=HelloWorldModule,
    # Internal name
    name="hello_world",
    # Name shown to users
    display_name="Hello, world",
    # Module's description
    description="Just an example!",
    # If the module can be displayed in the Today card
    allow_today=True,
    # If the module can be displayed as a card on the main screen
    allow_card=True,
)
```

TrashDash doesn't know about this module yet. To tell it about the module, we'll need to edit `trash_dash/modules/__init__.py`.

```python
# trash_dash/modules/__init__.py

"""Contains a repository of modules"""
from typing import Any, Dict

from trash_dash.modules.covid import CovidModule
from trash_dash.modules.example import MyModule
from trash_dash.modules.hacker_news import HackerNewsModule
from trash_dash.modules.news import NewsModule
from trash_dash.modules.todo import TodoModule
from trash_dash.modules.wakatime import WakatimeModule
from trash_dash.modules.weather import WeatherModule
# 1. import your module
from trash_dash.modules.hello_world import HelloWorldModule

# Type: module_name: module_class
modules: Dict[str, Any] = {
    MyModule.meta.name: MyModule,
    HackerNewsModule.meta.name: HackerNewsModule,
    WeatherModule.meta.name: WeatherModule,
    NewsModule.meta.name: NewsModule,
    WakatimeModule.meta.name: WakatimeModule,
    TodoModule.meta.name: TodoModule,
    CovidModule.meta.name: CovidModule,
    # 2. Add it to the `modules` dict
    # The name is fetched automatically
    HelloWorldModule.meta.name: HelloWorldModule
}
```

And that's all it takes to create a module, but wait! The module can't be displayed in `Today`, as a card of its own, or on its own screen yet. To get started on that front, see [`today()`, `card()` and `display()`](/modules/today-card-display)
