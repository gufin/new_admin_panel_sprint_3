from abc import ABC
from collections import defaultdict
from typing import Dict

from core.models import (
    BasePersonElastic,
    Filmwork,
    FilmworkElastick,
    GenreElastic,
    GenreFilmwork,
    Person,
    PersonElastic,
    PersonFilmWork,
)
from core.settings import logging


class PostgresTransform(ABC):
    @staticmethod
    def __get_base_data(record, mapper, result, parser):
        try:
            item = mapper(**record)
        except Exception as e:
            logging.error(e)
            return None, None, result
        data = result[item.id]
        if not data:
            data = parser(**item.dict())
        return item, data, result

    @staticmethod
    def __get_mapping_persons(role, data):
        current_attr = f'{role}s'
        if current_attr not in data.dict().keys():
            return None

        return {
            'names': getattr(data, f'{current_attr}_names'),
            'persons': getattr(data, current_attr)
        }

    def __add_role_person(self, role, data, film):
        try:
            person = Person(**film)
        except Exception as e:
            logging.error(e)
        if data_mapping := self.__get_mapping_persons(role, data):
            if person.name not in data_mapping['names']:
                data_mapping['names'].add(person.name)
                data_mapping['persons'].append(
                    BasePersonElastic(**person.dict()))

    def transform_film(self, records) -> Dict:
        result = defaultdict(dict)
        for record in records:
            film, data, result = self.__get_base_data(record, Filmwork, result,
                                                      FilmworkElastick)
            if not film:
                continue

            genre_name = film.genre_name
            if genre_name and genre_name not in data.genre:
                data.genre.add(genre_name)

            if film.role:
                self.__add_role_person(film.role, data, record)

            result[film.id] = data
        return result

    def transform_persons(self, records) -> Dict:
        result = defaultdict(dict)
        for record in records:
            person, data, result = self.__get_base_data(record, PersonFilmWork,
                                                        result, PersonElastic)
            if not person:
                continue

            data.role.add(person.role_str)
            data.film_ids.add(person.film_work_id)
            result[person.id] = data
        return result

    def transform_genres(self, records) -> Dict:
        result = defaultdict(dict)
        for record in records:
            genre, data, result = self.__get_base_data(record, GenreFilmwork,
                                                       result, GenreElastic)
            if not genre:
                continue

            data.description = genre.description
            data.film_ids.add(genre.film_work_id)
            result[genre.id] = data
        return result
