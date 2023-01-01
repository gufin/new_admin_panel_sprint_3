import logging

import psycopg2

from core.utils.backoff import backoff
from core.utils.data import DbLoader


class PostgresConnector(DbLoader):
    def __init__(self, logger=None) -> None:
        super().__init__(logger=logger)
        self.cursor = None

    @backoff(logger=logging)
    def query(self, sql_query: str) -> list:
        try:
            self.cursor.execute(sql_query)
        except psycopg2.OperationalError:
            self.logger.error('Error link to postgres database.')
            self.connect()
            self.cursor.execute(sql_query)
        return self.cursor.fetchall()
