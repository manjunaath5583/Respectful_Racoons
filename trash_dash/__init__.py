from rich.layout import Layout
from rich.live import Live

layout = Layout()

try:
    with Live(layout, screen=True) as live:
        while True:
            pass
except KeyboardInterrupt:
    pass
