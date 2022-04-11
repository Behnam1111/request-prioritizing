from sqlalchemy import Column, String, Integer, MetaData, create_engine, inspect, Table
from config.runtime_config import RuntimeConfig
from dao.base_dao import BaseDao
from model.request_model import Request


class RequestDao(BaseDao):

    def __init__(self):
        super(RequestDao, self).__init__()
        self.model = Request

    @staticmethod
    def create_table():
        engine = create_engine(
            "mysql://{username}:{password}@{host}/{schema}".format(username=RuntimeConfig.DB_USERNAME,
                                                                   password=RuntimeConfig.DB_PASSWORD,
                                                                   host=RuntimeConfig.DB_HOST,
                                                                   schema=RuntimeConfig.DB_SCHEMA), echo=False)
        insp = inspect(engine)
        if not insp.has_table(engine, "requests"):
            metadata_obj = MetaData()
            Table("requests", metadata_obj,
                  Column('id', Integer, primary_key=True, nullable=False),
                  Column('status', String(50)),
                  Column('result', String(200)),
                  Column('user_id', Integer)
                  )
            metadata_obj.create_all(engine)

    def add(self, status, user_id):
        request = Request(status=status, user_id=user_id)
        self.session.add(request)
        self.session.commit()
        return request.id

    def get_status_of_request(self, request_id):
        request = self.session.query(self.model).filter(self.model.id == request_id).first().status
        return request

    def get_result_of_completed_request(self, request_id):
        status = self.session.query(self.model).filter(self.model.id == request_id).first().status
        if status:
            return self.session.query(self.model).filter(self.model.id == request_id).first().result

    def set_result_for_request(self, request_id, result):
        request = self.session.query(self.model).filter(self.model.id == request_id).first()
        request.status = 'Finished'
        request.result = result
        self.session.commit()

    def get_last_request(self):
        last_request = self.session.query(self.model).order_by(self.model.id)[-1]
        if last_request:
            last_request = last_request.id
        else:
            last_request = 1
        return last_request

