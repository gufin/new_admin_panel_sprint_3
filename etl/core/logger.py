import logging

logging.basicConfig(
    filename='loader.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)