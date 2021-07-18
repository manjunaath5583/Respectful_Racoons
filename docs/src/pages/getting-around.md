---
title: "Getting around in TrashDash"
layout: ../layouts/Main.astro
---

TrashDash uses only the keyboard to navigate. There are certain keystrokes that you'll have to press to navigate around the dashboard. They're hinted to you, but we've put a list of keystrokes that'll allow you to navigate.

**Keystrokes that work everywhere**:

- `q` - Exits TrashDash
- `ESC` - Returns to the Main Menu
- `a` - Shows all modules
- `s` - Opens `settings.toml` in your default editor

**Keystrokes that work on the main screen**:

- `1` - Go to the main page of the module shown on the first card.
- `2` - Go to the main page of the module shown on the second card.
- `3` - Go to the main page of the module shown on the third card.

**Module specific keystrokes**:

Module specific keystrokes only work on that module's page and will be hinted to you on the screen.

## Modules can seize keystrokes

Modules can seize keystrokes. This means that they can prevent the `a`, `s`, and `q` key from working as intended. This is to get user data, or to listen to these keys. The `ESC` key still works, so you can return to the main screen when a module has seized keystrokes.
