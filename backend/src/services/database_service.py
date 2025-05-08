from contextlib import contextmanager
from sqlmodel import Session
from src.core import config
from src.core import logging


@contextmanager
def get_session():
    try:
        session = Session(config.engine)
        yield session
    except Exception as e:
        logging.logger.error(str(e))
    finally:
        session.commit()
        session.close()
