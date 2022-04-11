from sqlalchemy import Column, String, Integer, MetaData, create_engine, inspect, Table
from config.runtime_config import RuntimeConfig
from dao.base_dao import BaseDao
from model.user_model import User


class UserDao(BaseDao):
    def __init__(self):
        super(UserDao, self).__init__()
        self.model = User

    @staticmethod
    def create_table():
        engine = create_engine(
            "mysql://{username}:{password}@{host}/{schema}".format(username=RuntimeConfig.DB_USERNAME,
                                                                   password=RuntimeConfig.DB_PASSWORD,
                                                                   host=RuntimeConfig.DB_HOST,
                                                                   schema=RuntimeConfig.DB_SCHEMA), echo=False)
        insp = inspect(engine)
        if not insp.has_table(engine, "users"):
            metadata_obj = MetaData()
            Table("users", metadata_obj,
                  Column('id', Integer, primary_key=True, nullable=False),
                  Column('user_weight', Integer)),

            metadata_obj.create_all(engine)

    def add(self, user_weight):
        user = User(user_weight)
        self.session.add(user)
        self.session.commit()
        return user.id
