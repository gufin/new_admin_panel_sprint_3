import datetime
import os

from dotenv import load_dotenv
from pydantic import BaseSettings

from core.constants import GENRES_SETTINGS, MOVIES_SETTINGS, PERSONS_SETTINGS

load_dotenv()


class AppSettings(BaseSettings):
    BLOCK_SIZE: int = 100
    TIME_TO_RESTART: int = 60
    DEFAULT_DATE: datetime.datetime = datetime.datetime(year=2020,
                                                        month=1,
                                                        day=1)
    FORMAT_DATE: str = '%Y-%m-%d %H:%M:%S'

    POSTGRES_DSL: dict = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', 5435),
        'options': '-c search_path=content'
    }

    REDIS_DSL: dict = {
        'host': os.environ.get('REDIS_HOST', 'localhost'),
        'port': os.environ.get('REDIS_PORT', 6379)
    }

    ELASTIC_DSL: dict = {
        'hosts': [
            f'http://{os.environ.get("ELASTIC_HOST", "localhost")}:'
            f'{os.environ.get("ELASTIC_PORT", 9200)}'
        ],
        'basic_auth': (
            os.environ.get('ELASTIC_USER'),
            os.environ.get('ELASTIC_PASSWORD')
        )
    }

    ELASTIC_INDEX: dict = {
        'movies': MOVIES_SETTINGS,
        'persons': PERSONS_SETTINGS,
        'genres': GENRES_SETTINGS
    }


app_settings = AppSettings()