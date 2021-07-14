"""Basic event emitter"""
from collections.abc import Callable
from typing import Any

_event_handlers = {}


def on(name: str, handler: Callable):
    """Register an event"""
    _event_handlers[name] = handler


def off(name: str):
    """Unregister an event"""
    if _event_handlers.get(name):
        _event_handlers.pop(name)


def emit(name: str, *args: Any):
    """Call the handler associated with the event"""
    handler = _event_handlers.get(name)
    if handler:
        handler(*args)
