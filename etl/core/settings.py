import datetime
import logging
import os

from dotenv import load_dotenv

from core.constants import GENRES_SETTINGS, MOVIES_SETTINGS, PERSONS_SETTINGS

load_dotenv()

BLOCK_SIZE = 100
TIME_TO_RESTART = 60
DEFAULT_DATE = datetime.datetime(year=2020, month=1, day=1)
FORMAT_DATE = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(
    filename='loader.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

POSTGRES_DSL = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', 5435),
    'options': '-c search_path=content'
}

REDIS_DSL = {
    'host': os.environ.get('REDIS_HOST', 'localhost'),
    'port': os.environ.get('REDIS_PORT', 6379)
}

ELASTIC_DSL = {
    'hosts': [
        f'http://{os.environ.get("ELASTIC_HOST", "localhost")}:'
        f'{os.environ.get("ELASTIC_PORT", 9200)}'
    ],
    'basic_auth': (
        os.environ.get('ELASTIC_USER'),
        os.environ.get('ELASTIC_PASSWORD')
    )
}

ELASTIC_INDEX = {
    'movies': MOVIES_SETTINGS,
    'persons': PERSONS_SETTINGS,
    'genres': GENRES_SETTINGS
}
