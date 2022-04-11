from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from model.base_model import Base
from model.user_model import User


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    status = Column(String)
    result = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', foreign_keys='Request.user_id')

    def __init__(self, status, user_id):
        self.status = status
        self.user_id = user_id
