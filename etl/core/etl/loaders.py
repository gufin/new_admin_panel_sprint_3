from typing import List

from core.connectors.postgres import PostgresConnector
from core.constants import SQL_TEMPLATES


class PostgresLoader(PostgresConnector):
    def __get_data(self, template, params, table_name=None):
        if table_name:
            sql_tmp = SQL_TEMPLATES.get(template).format(table_name, table_name)
        else:
            sql_tmp = SQL_TEMPLATES.get(template)
        sql = self.cursor.mogrify(sql_tmp, params)
        return self.query(sql)

    def read_table(self,
                   table: str,
                   date: str,
                   limit: int,
                   offset: int = 0):
        while True:
            params = {
                'date': date,
                'limit': limit,
                'offset': offset
            }
            table_ids = self.__get_data('table_id', params, table_name=table)
            if not table_ids:
                break
            yield table_ids

            offset += limit
            if len(table_ids) != limit:
                break

    def get_person_data(self, ids: List):
        return self.__get_data(
            template='person_id',
            params={'persons_ids': tuple(ids)}
        )

    def get_genre_data(self, ids: List):
        return self.__get_data(
            template='genre_id',
            params={'genres_ids': tuple(ids)}
        )

    def get_film_data(self, film_ids: List):
        return self.__get_data(template='films', params={
            'films_id': tuple(film_ids)}) if film_ids else None

    def get_film_id_in_table(self, table: str, table_ids: List):
        return self.__get_data(
            template='related_film_id',
            params={'ids': tuple(table_ids)},
            table_name=table
        )
