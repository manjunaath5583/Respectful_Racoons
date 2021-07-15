"""Wrapper for accessing data for modules"""
import os

from tinydb import TinyDB


def _get_path(file_name: str) -> str:
    """Gets a path relative to this file"""
    return os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), f"data/{file_name}.data.json"
        )
    )


class Data:
    __module_name: str
    __path: str
    __db: TinyDB

    def __create_db(self) -> None:
        """Creates and inits the database"""
        self.__path = _get_path(self.__module_name)
        self.__db = TinyDB(self.__path)

    def __init__(self, module_name: str):
        self.__module_name = module_name
        self.__create_db()

    @property
    def db(self):
        """The TinyDB database"""
        return self.__db

    @property
    def module_name(self):
        """The name of the module"""
        return self.__module_name


d = Data("test")
print(d.db)
