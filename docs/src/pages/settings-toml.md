---
title: "Editing TrashDash's settings"
layout: ../layouts/Main.astro
---

TrashDash follows the [Sublime Text](https://sublimetext.com) approach and allows you to directly edit the settings file.

TrashDash's settings are stored in [TOML](https://toml.io), a syntax very similar to Python's ConfigParser (`.ini`) format.

It has been choosen because it is more readable than JSON, and it doesn't require indentation, unlike YAML.

To edit your settings, press `s` at any screen.

An example `settings.toml`:

```toml
app_name = "TrashDash"
cards = [ "todo", "hacker_news", "news" ]

[modules]

[module.test]
name = "test"

[module.today]
name = "today"

[module.weather]
name = "weather"
ip = "xxx.xxx.xxx.xxx"

[module.news]
name = "news"

[module.hacker_news]
name = "hacker_news"

[module.example_module]
name = "example_module"

[module.wakatime]
name = "wakatime"
username = "xxxxxxxx"

[module.todo]
name = "todo"

[module.covid]
name = "covid"
```

## An overview

Let's go step by step through every key in `settings.toml`:

- `app_name` is the text that will show up in the far left of the main screen. This allows you to customise your dashboard.
- `cards` is the list of cards that will appear on the main screen. This list can contain between 0-3 items and the items must be the **internal name** of the module.

> Tip: To see the internal name of the module, you can just see the part after `[module.]` in `settings.toml`. For example, the Covid 19 module has an internal anme of `covid`, shown in `[module.covid]`.

## Module specific settings

You can edit settings of modules under their respective keys. If I wanted to edit the settings of the Wakatime module, I would edit the keys under `[module.wakatime]`. The only built-in modules that support their own settings are `weather` and `wakatime`.

- `[module.weather]`s `ip` key should contain your IP. This is used to fetch the weather information of your location. This is auto-detected when you start TrashDash for the first time.
- `[module.wakatime]`s `username` key should contain your username. This is used to fetch your wakatime stats.

> TrashDash may **CRASH** if `settings.toml` is invalid!
