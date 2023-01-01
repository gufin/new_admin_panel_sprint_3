import elasticsearch
from elasticsearch import Elasticsearch, helpers
from pydantic.main import BaseModel

from core.logger import logging
from core.settings import app_settings
from core.utils.backoff import backoff
from core.utils.data import DbLoader


class ESLoader(DbLoader):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.connect()

    @backoff(logger=logging)
    def connect(self) -> None:
        self.connection = Elasticsearch(**app_settings.ELASTIC_DSL)
        self.__check_and_create_index()

    def __check_and_create_index(self) -> None:
        for name, index_setting in app_settings.ELASTIC_INDEX.items():
            if not self.connection.indices.exists(index=name):
                self.connection.indices.create(**index_setting)

    @backoff(logger=logging)
    def set_bulk(self, index: str, data) -> None:
        try:
            helpers.bulk(self.connection,
                         self.generate_elastic_data(index, data))
        except elasticsearch.exceptions.ConnectionError:
            self.logger.error('Error to connect ElasticSearch.')
            self.connect()
            helpers.bulk(self.connection,
                         self.generate_elastic_data(index, data))

    @staticmethod
    def generate_elastic_data(index, data: list[BaseModel]) -> None:
        for item in data:
            yield {
                '_index': index,
                '_id': item.uuid,
                '_source': item.json()
            }
