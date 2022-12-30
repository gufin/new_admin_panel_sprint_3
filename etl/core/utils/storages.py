import abc
import json
import os
from typing import Optional


class BaseStorage(abc.ABC):
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path
        self.data = self.retrieve_state()

    def retrieve_state(self) -> dict:
        if not os.path.exists(self.file_path):
            return dict()
        with open(self.file_path, 'r') as json_file:
            data = json.load(json_file)
        return data or dict()

    def save_state(self, state) -> None:
        with open(self.file_path, 'w') as json_file:
            json.dump(state, json_file)
