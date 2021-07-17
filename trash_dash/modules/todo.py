from collections.abc import Callable
from typing import Any, List, Literal, Optional, TypedDict, cast

from blessed.keyboard import Keystroke
from rich.align import Align
from rich.columns import Columns
from rich.console import RenderableType, RenderGroup
from rich.layout import Layout
from rich.padding import Padding
from rich.panel import Panel
from tinydb.database import Document

from trash_dash.console import console
from trash_dash.data import Data
from trash_dash.events import emit, off, on, once
from trash_dash.module import Module, register_module

keys: str = ""
showing_prompt: bool = False
prompt_layout = RenderGroup(
    Align("Press [b]m[/b] to move items", "center"),
    Align("Press [b]x[/b] to delete items", "center"),
    Align("Press [b]ESC[/b] to go back", "center"),
)
get_prompt: Optional[Callable] = None


def prompt(layout: Layout, msg: str, evt: str, payload: tuple = tuple()):
    global showing_prompt

    emit("seize_keystrokes", True)
    showing_prompt = True

    def get_prompt_msg(message: str) -> RenderableType:
        return RenderGroup(
            (keys if len(keys) > 0 else f"[gray]{message}[/gray]"),
            "Press [b]ENTER[/b] to confirm and clear out the text to cancel.",
        )

    def remove_prompt():
        global showing_prompt
        emit("seize_keystrokes", False)
        showing_prompt = False
        layout.update(prompt_layout)

    def handler(key: Keystroke, event: str, *args: Any):
        global keys
        if not key.is_sequence:
            keys += key
        elif key.name == "KEY_ENTER":
            emit(f"todo.{event}", keys, *args)
            keys = ""
            off("todo.keystroke")
            emit("todo.remove_prompt")
        elif key.name == "KEY_BACKSPACE":
            if len(keys) > 0:
                keys = keys[0:-1]
            elif not keys:
                emit(f"todo.remove_prompt")

    on("todo.keystroke", lambda x: handler(x, evt, *payload))
    once("todo.remove_prompt", remove_prompt)
    layout.update(get_prompt_msg(msg))

    return lambda: get_prompt_msg(msg)


class TodoType(TypedDict):
    id: str
    text: str
    stage: Literal["todo", "doing", "done"]


class Todo:
    data: Data

    def __init__(self):
        self.data = Data("todo")

    def add_item(self, text: str, stage: Literal["todo", "doing", "done"]):
        todo = dict(text=text, stage=stage)
        todo_id = self.data.db.insert(todo)
        doc = self.data.db.get(doc_id=todo_id)
        return self.parse(doc)

    def delete_item(self, todo_id: int):
        try:
            self.data.db.remove(doc_ids=(todo_id,))
        except KeyError:
            return

    def get_item(self, todo_id: int) -> Optional[Document]:
        return self.data.db.get(doc_id=todo_id)

    def move_item(self, todo_id: int, stage: Literal["todo", "doing", "done"]):
        item = self.get_item(todo_id)
        if not item:
            return  # type: ignore
        item["stage"] = stage
        self.data.db.update(item, doc_ids=(todo_id,))

    @staticmethod
    def parse(data: Document) -> TodoType:
        return cast(
            TodoType,
            {
                "text": data.get("text"),
                "stage": data.get("stage"),
                "id": str(data.doc_id),
            },
        )

    @property
    def tasks(self) -> List[TodoType]:
        return list(map(self.parse, self.data.db.all()))

    @property
    def todo(self) -> List[TodoType]:
        return list(filter(lambda x: x["stage"] == "todo", self.tasks))

    @property
    def doing(self) -> List[TodoType]:
        return list(filter(lambda x: x["stage"] == "doing", self.tasks))

    @property
    def done(self) -> List[TodoType]:
        return list(filter(lambda x: x["stage"] == "done", self.tasks))


class TodoModule(Module):
    @classmethod
    def display(cls):
        todo = Todo()
        layout = Layout(name="todo.main")
        layout_tasks = Layout(name="todo.tasks")
        layout_prompt = Layout(prompt_layout, name="todo.prompt", size=3)
        layout.split_column(layout_tasks, layout_prompt)

        def get_todos() -> RenderableType:
            to_do = todo.todo
            doing = todo.doing
            done = todo.done
            todo_r = Padding(
                RenderGroup(
                    *list(map(lambda x: f"[b]{x.get('id')}[/] {x.get('text')}", to_do)),
                    Padding("Press [b]t[/] to add item", (1, 0, 0, 0)),
                ),
                (1, 2),
            )
            doing_r = Padding(
                RenderGroup(
                    *list(map(lambda x: f"[b]{x.get('id')}[/] {x.get('text')}", doing)),
                    Padding("Press [b]d[/] to add item", (1, 0, 0, 0)),
                ),
                (1, 2),
            )
            done_r = Padding(
                RenderGroup(
                    *list(map(lambda x: f"[b]{x.get('id')}[/] {x.get('text')}", done)),
                    Padding("Press [b]n[/] to add item", (1, 0, 0, 0)),
                ),
                (1, 2),
            )
            return Columns(
                [
                    Panel(todo_r, title="To Do"),
                    Panel(doing_r, title="Doing"),
                    Panel(done_r, title="Done"),
                ],
                width=(console.width // 3) - 3,
            )

        layout_tasks.update(get_todos())

        def handler(key: Keystroke):
            global get_prompt
            if showing_prompt:
                return
            if key == "t":
                off("todo.keystroke")
                get_prompt = prompt(
                    layout["todo.prompt"], "Type item to add to Todo", "add", ("todo",)
                )
            elif key == "d":
                off("todo.keystroke")
                get_prompt = prompt(
                    layout["todo.prompt"],
                    "Type item to add to Doing",
                    "add",
                    ("doing",),
                )
            elif key == "n":
                off("todo.keystroke")
                get_prompt = prompt(
                    layout["todo.prompt"], "Type item to add to Done", "add", ("done",)
                )
            elif key == "x":
                off("todo.keystroke")
                get_prompt = prompt(
                    layout["todo.prompt"], "Type item number to delete", "delete"
                )
            elif key == "m":
                off("todo.keystroke")
                get_prompt = prompt(
                    layout["todo.prompt"],
                    "Type item number to move, and the location, separated by a space. (e.g. 1 done)",
                    "move",
                )

        def add_item(item: str, stage: Literal["todo", "doing", "done"]):
            global get_prompt
            todo.add_item(item, stage)
            get_prompt = None
            layout_tasks.update(get_todos())

        def delete_item(item: str):
            global get_prompt
            if not item.isnumeric():
                return
            todo.delete_item(int(item))
            get_prompt = None
            layout_tasks.update(get_todos())

        def move_item_1(payload: str):
            global get_prompt
            try:
                item_id, stage = payload.split()
                if not item_id.isnumeric() or stage not in ["todo", "doing", "done"]:
                    return
                todo.move_item(int(item_id), stage)
                get_prompt = None
                layout_tasks.update(get_todos())
            except ValueError:
                return

        on("todo.keystroke", handler)
        on("todo.add", add_item)
        on("todo.delete", delete_item)
        on("todo.move", move_item_1)

        def update():
            if showing_prompt and get_prompt is not None:
                layout["todo.prompt"].update(get_prompt())
                emit("todo.update", layout)
            elif not showing_prompt:
                on("todo.keystroke", handler)

        on("todo.event_loop", update)

        return layout

    @staticmethod
    def card():
        todo = Todo()
        return RenderGroup("[b]Your tasks:", *list(map(lambda x: x["text"], todo.todo)))

    @staticmethod
    def today():
        todo = Todo()
        tasks = [*todo.todo, *todo.doing]
        length = len(tasks)
        return RenderGroup(f"[b]{length}[/] {'tasks' if length != 1 else 'task'} left!")


register_module(TodoModule, "todo", "To Do", "A Todo List", True, True)
