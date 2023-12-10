from functools import wraps

from ..db import connect, initialize_database, logger


def init_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        initialize_database()
        return func(*args, **kwargs)

    return wrapper


def connect_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        logger.debug("Connecting to database")
        conn = connect()
        conn.autocommit = True
        try:
            kwargs["conn"] = conn
            result = func(*args, **kwargs)
        finally:
            logger.debug("Closing")
            conn.close()
        return result

    return wrapper
