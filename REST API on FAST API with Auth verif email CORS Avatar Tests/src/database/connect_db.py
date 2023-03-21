# import configparser
# import pathlib

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings

# config_file = pathlib.Path(__file__).parent.parent.parent.joinpath("config.ini")
# config = configparser.ConfigParser()
# config.read(config_file)
#
# username = config.get('DB', 'user')
# password = config.get('DB', 'password')
# db_name = config.get('DB', 'db_name')
# host = config.get('DB', 'host')
# port = config.get('DB', 'port')

# SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


# Dependency
def get_db():
    """
    The get_db function is a context manager that returns the database session.
    It also ensures that the connection to the database is closed after each request.

    :return: A database session
    :doc-author: Trelent
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
