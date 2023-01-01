import abc
from typing import Any

from core.utils.storages import BaseStorage


class DbLoader(abc.ABC):
    """Класс для работы с базой данных."""

    def __init__(self, logger=None):
        self.connection = None
        self.logger = logger

    @abc.abstractmethod
    def connect(self):
        pass


class State():

    def __init__(self, storage: BaseStorage) -> None:
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        state = self.storage.retrieve_state().get(key)
        if state:
            state = state.decode()
        return state or None
