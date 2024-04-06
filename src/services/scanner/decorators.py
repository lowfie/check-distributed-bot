import time
import logging


def async_never_fall(func):
    async def wrapper(self, *args, **kwargs):
        while True:
            try:
                await func(self, *args, **kwargs)
            except Exception as e:
                logging.exception(e.__str__)
                time.sleep(60)

    return wrapper
