"""Contains a repository of modules"""
from typing import Any, Dict

from trash_dash.modules.hacker_news import HackerNewsModule

# Type: module_name: module_class
modules: Dict[str, Any] = {HackerNewsModule.meta.name: HackerNewsModule}
