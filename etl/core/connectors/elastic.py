import elasticsearch
from elasticsearch import Elasticsearch, helpers
from pydantic.main import BaseModel

from core.settings import ELASTIC_DSL, ELASTIC_INDEX, logging
from core.utils.backoff import backoff
from core.utils.data import DbLoader


class ESLoader(DbLoader):
    def __init__(self, logger=None):
        super(ESLoader, self).__init__(logger)
        self.connect()

    @backoff(logger=logging)
    def connect(self):
        self.connection = Elasticsearch(**ELASTIC_DSL)
        self.__check_and_create_index()

    def __check_and_create_index(self):
        for name, index_setting in ELASTIC_INDEX.items():
            if not self.connection.indices.exists(index=name):
                self.connection.indices.create(**index_setting)

    @backoff(logger=logging)
    def set_bulk(self, index, data):
        try:
            helpers.bulk(self.connection,
                         self.generate_elastic_data(index, data))
        except elasticsearch.exceptions.ConnectionError:
            self.logger.error('Error to connect ElasticSearch.')
            self.connect()
            helpers.bulk(self.connection,
                         self.generate_elastic_data(index, data))

    @staticmethod
    def generate_elastic_data(index, data: list[BaseModel]):
        for item in data:
            yield {
                '_index': index,
                '_id': item.uuid,
                '_source': item.json()
            }
