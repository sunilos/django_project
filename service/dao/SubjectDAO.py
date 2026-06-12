from service.models import Subject
from service.utility.DataValidator import DataValidator
from .BaseDAO import BaseDAO


class SubjectDAO(BaseDAO):

    def get_model(self):
        return Subject
