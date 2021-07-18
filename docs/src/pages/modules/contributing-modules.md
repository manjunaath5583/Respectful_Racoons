---
title: Contributing modules
layout: ../../layouts/Main.astro
---

Thank you for deciding to contribute your module to the TrashDash project!

There are however, a few guidelines you'll have to follow to ensure that the code style isn't different between modules.

> Please use `poetry` for package management!

1. Turn on `pre-commit`

```shell
$ poetry run pre-commit install
```

This will ensure that your code is formatted and error-free upon committing

2. Run `mypy` at the end

```shell
$ poetry run mypy trash_dash main.py
```

MyPy will check for type errors.

3. Make sure your branch has the pattern `add-module-module_name`.

4. PR away!
