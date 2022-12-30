import logging
from functools import wraps
from time import sleep


def backoff(
        start_sleep_time=0.1,
        factor=2,
        border_sleep_time=10,
        logger=logging
):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            wait_time = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(
                        f'Error execute function({func.__name__}): {e}')
                    if wait_time >= border_sleep_time:
                        wait_time = border_sleep_time
                    else:
                        wait_time = min(wait_time * factor, border_sleep_time)
                    sleep(wait_time)

        return inner

    return func_wrapper
