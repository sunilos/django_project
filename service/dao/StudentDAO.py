from service.models import Student
from .BaseDAO import BaseDAO


class StudentDAO(BaseDAO):

    def get_model(self):
        return Student
