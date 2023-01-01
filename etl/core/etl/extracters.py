import json
from datetime import datetime
from typing import Optional

from core.connectors.elastic import ESLoader
from core.etl.loaders import PostgresLoader
from core.etl.transformers import PostgresTransform
from core.settings import app_settings
from core.utils.data import State


class ElasticExtract:
    RELATED_TABLES = ['person', 'genre']

    def __init__(self, state: State, pg: PostgresLoader, es: ESLoader,
                 table_name: str) -> None:
        self.state = state
        self.pg: PostgresLoader = pg
        self.es = es
        self.table_name: str = table_name

    @staticmethod
    def __get_transformer_func(table_name):
        if table_name == 'person':
            return PostgresTransform().transform_persons
        elif table_name == 'genre':
            return PostgresTransform().transform_genres
        return None

    def __get_index_name(self, table_name: str) -> Optional[bool]:
        return f'{table_name}s' if table_name in self.RELATED_TABLES else None

    def __is_related(self, table_name: str) -> bool:
        return table_name in self.RELATED_TABLES

    def __get_data_func(self, table_name: str):
        if table_name == 'person':
            return self.pg.get_person_data
        elif table_name == 'genre':
            return self.pg.get_genre_data
        return None

    def load_data(self):
        limit = app_settings.BLOCK_SIZE
        state_table = {}
        if state_table_raw := self.state.get_state(self.table_name):
            state_table = json.loads(state_table_raw)
        date_start = state_table.get('date', app_settings.DEFAULT_DATE)
        if isinstance(date_start, str):
            date_start = datetime.strptime(date_start, app_settings.FORMAT_DATE)
        offset_start = state_table.get('offset', 0)
        date_end = date_start

        for modified_ids in self.pg.read_table(self.table_name, date_start,
                                               limit, offset_start):
            date_end = datetime.now().strftime(app_settings.FORMAT_DATE)
            offset_start += limit
            if self.__is_related(self.table_name):
                film_modified_ids = self.pg.get_film_id_in_table(
                    self.table_name, [item['id'] for item in modified_ids]
                )
                data = self.__get_data_func(self.table_name)(
                    [item['id'] for item in modified_ids]
                )
                serialize_data_index = self.__get_transformer_func(
                    self.table_name)(data)
                self.es.set_bulk(
                    self.__get_index_name(self.table_name),
                    serialize_data_index.values()
                )
            else:
                film_modified_ids = modified_ids

            if film_result := self.pg.get_film_data(
                    [item['id'] for item in film_modified_ids]):
                film_serialize = PostgresTransform().transform_film(film_result)
                self.es.set_bulk('movies', film_serialize.values())
            self.state.set_state(self.table_name, json.dumps({
                'offset': offset_start,
                'date': date_start.strftime(app_settings.FORMAT_DATE)
            }))

        self.state.set_state(self.table_name, json.dumps({
            'offset': 0,
            'date': date_end if isinstance(date_end,
                                           str) else date_end.strftime(
                app_settings.FORMAT_DATE)
        }))
        return self.state
