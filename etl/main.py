from time import sleep

from core.connectors.elastic import ESLoader
from core.connectors.postgres import PostgresConnector
from core.connectors.redis import RedisStorage
from core.etl.extracters import ElasticExtract
from core.etl.loaders import PostgresLoader
from core.settings import logging, TIME_TO_RESTART
from core.utils.data import State


def load_data(state: State, pg: PostgresConnector, es: ESLoader) -> None:
    tables = ['genre', 'person', 'film_work']
    for table_name in tables:
        logging.info(f'Table "{table_name}": start loading')
        extract = ElasticExtract(state, pg, es, table_name)
        state = extract.load_data()
        logging.info(f'Table "{table_name}": end loading')


if __name__ == '__main__':
    redis_state = State(RedisStorage(logger=logging))
    pg_loader = PostgresLoader(logger=logging)
    es_loader = ESLoader(logger=logging)

    while True:
        load_data(redis_state, pg_loader, es_loader)
        sleep(TIME_TO_RESTART)
