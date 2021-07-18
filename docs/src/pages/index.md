---
title: Welcome to TrashDash's documentation
layout: ../layouts/Main.astro
---

<img src="/ss.png" alt="Screenshot of TrashDash" style="width: 100%; border: 1px black solid; border-radius: 0.5rem" />

# TrashDash

> The trashiest dashboard you'll ever find!

TrashDash is a command line dashboard that organizes all of your data into one place. Just open it up to see everything in a neat view.

# Installation instructions

Python 3.9 is required. Any OS will do

TrashDash is pretty easy to install.

First, clone this repository:

```shell
git clone https://github.com/manjunaath5583/respectful_racoons.git trashdash

cd trashdash
```

Next, install all dependencies:

```bash
# Feel free to create a Virtual Environment, if you don't like clutter
pip install -r requirements.txt

# Or if you're extra hip, you can use poetry
poetry install
```

Finally, run the application

```bash
# Don't forget to activate the Virtual Environment (if you created one)
python3 main.py

# Or if you use poetry,
poetry run python3 main.py
```

On first start, TrashDash may take a bit of while (5-20 seconds) to start. This is because TrashDash is fetching APIs and caching them. This only happens once a day, so you should only have to wait once in a while.

# Troubleshooting

If you get any errors, try deleting any `.data.json` files you find in the `trash_dash/data` folder.

If the content gets cropped, try reducing the size of the terminal!
