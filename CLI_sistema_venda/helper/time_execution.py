from functools import wraps
import time
from helper.logger_file import logger

def time_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.perf_counter() - start
            logger.info(f"executado em {duration:.6f}s \n")
    return wrapper