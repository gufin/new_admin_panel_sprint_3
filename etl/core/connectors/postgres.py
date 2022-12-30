import logging

import psycopg2
from psycopg2.extras import DictCursor

from core.settings import POSTGRES_DSL
from core.utils.backoff import backoff
from core.utils.data import DbLoader


class PostgresConnector(DbLoader):
    def __init__(self, logger=None):
        super(PostgresConnector, self).__init__(logger=logger)
        self.cursor = None
        self.connect()

    @backoff(logger=logging)
    def connect(self):
        self.connection = psycopg2.connect(**POSTGRES_DSL,
                                           cursor_factory=DictCursor)
        self.cursor = self.connection.cursor()

    @backoff(logger=logging)
    def query(self, sql_query: str):
        try:
            self.cursor.execute(sql_query)
        except psycopg2.OperationalError:
            self.logger.error('Error link to postgres database.')
            self.connect()
            self.cursor.execute(sql_query)
        return self.cursor.fetchall()
