from redis import exceptions, Redis

from core.settings import logging, REDIS_DSL
from core.utils.backoff import backoff
from core.utils.data import DbLoader
from core.utils.storages import BaseStorage


class RedisStorage(DbLoader, BaseStorage):

    def __init__(self, logger):
        super(RedisStorage, self).__init__(logger=logger)
        self.connect()

    @backoff(logger=logging)
    def connect(self):
        self.connection = Redis(**REDIS_DSL)

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
