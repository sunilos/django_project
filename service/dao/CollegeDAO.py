from service.models import College
from .BaseDAO import BaseDAO


class CollegeDAO(BaseDAO):

    def get_model(self):
        return College

    def get_Unique(self):
        return ["name"]
