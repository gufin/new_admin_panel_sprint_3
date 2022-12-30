import datetime
from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseModel
from pydantic.fields import Field


class PersonFilmRole(Enum):
    ACTOR = 'actor'
    SOUND_DIRECTOR = 'sound_director'
    DIRECTOR = 'director'
    MUSIC_EDITOR = 'music_director'
    WRITER = 'writer'


class Person(BaseModel):
    id: str
    name: str = Field(alias='full_name')


class PersonFilmWork(Person):
    role_str: Optional[str] = Field(alias='role')
    film_work_id: Optional[str]


class BasePersonElastic(BaseModel):
    uuid: str = Field(alias='id')
    full_name: str = Field(alias='name')


class PersonElastic(BasePersonElastic):
    role: Set[str] = set()
    film_ids: Set[str] = set()


class Genre(BaseModel):
    id: str
    name: str


class GenreFilmwork(Genre):
    description: Optional[str]
    film_work_id: str


class GenreElastic(BaseModel):
    uuid: str = Field(alias='id')
    name: str
    description: Optional[str]
    film_ids: Set[str] = set()


class Filmwork(BaseModel):
    id: str = Field(alias='fw_id')
    title: str
    description: Optional[str]
    rating: Optional[float]
    type: str
    created: datetime.datetime
    modified: datetime.datetime
    role: Optional[str]
    person_id: Optional[str] = Field(alias='id')
    person_name: Optional[str] = Field(alias='full_name')
    genre_id: Optional[str] = Field(alias='genre_id')
    genre_name: Optional[str] = Field(alias='name')


class FilmworkElastick(BaseModel):
    uuid: str = Field(alias='id')
    title: str
    description: Optional[str]
    imdb_rating: Optional[float] = Field(alias='rating', default=0)
    created: datetime.datetime
    genre: Set = set()
    directors: List[BasePersonElastic] = []
    directors_names: Set = set()
    actors: List[BasePersonElastic] = []
    actors_names: Set = set()
    writers: List[BasePersonElastic] = []
    writers_names: Set = set()
