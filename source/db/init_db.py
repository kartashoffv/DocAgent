from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

from source.config import config


def init_db():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database {getattr(config, 'POSTGRES_DB', 'DEFAULT_DB')} created successfully!")
    else:
        print(f"Database {getattr(config, 'POSTGRES_DB', 'DEFAULT_DB')} already exists")


if __name__ == "__main__":
    init_db()
