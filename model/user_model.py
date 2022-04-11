from sqlalchemy import Integer, Column, ForeignKey

from model.base_model import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_weight = Column(Integer)

    def __init__(self, user_weight):
        self.user_weight = user_weight
