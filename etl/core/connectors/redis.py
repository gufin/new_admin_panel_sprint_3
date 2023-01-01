from redis import exceptions, Redis

from core.logger import logging
from core.settings import app_settings
from core.utils.backoff import backoff
from core.utils.data import DbLoader
from core.utils.storages import BaseStorage


class RedisStorage(DbLoader, BaseStorage):

    def __init__(self, logger: logging) -> None:
        super().__init__(logger=logger)
        self.connect()

    @backoff(logger=logging)
    def connect(self) -> None:
        self.connection = Redis(**app_settings.REDIS_DSL)

    @backoff(logger=logging)
    def save_state(self, state: dict) -> None:
        try:
            self.connection.mset(state)
        except exceptions.ConnectionError as e:
            self.logger.error(f'Error to connect Redis: {e}')
            self.connect()
            self.connection.mset(state)

    @backoff(logger=logging)
    def retrieve_state(self) -> Redis:
        try:
            self.connection.ping()
        except exceptions.ConnectionError as e:
            self.logger.error(f'Error to connect Redis: {e}')
            self.connect()
        return self.connection
