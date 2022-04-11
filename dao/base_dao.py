import sqlalchemy as db

from sqlalchemy.orm import scoped_session, sessionmaker

from config.runtime_config import RuntimeConfig

from sqlalchemy_utils import create_database, database_exists


class BaseDao:
    def __init__(self):
        url = "mysql://{username}:{password}@{host}/{schema}".format(username=RuntimeConfig.DB_USERNAME,
                                                                     password=RuntimeConfig.DB_PASSWORD,
                                                                     host=RuntimeConfig.DB_HOST,
                                                                     schema=RuntimeConfig.DB_SCHEMA)
        if not database_exists(url):
            create_database(url)

        engine = db.create_engine(url)

        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=engine))
        self.conn = engine.connect()
        self.model = None
