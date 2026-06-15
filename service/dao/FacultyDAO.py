from service.models import Faculty
from .BaseDAO import BaseDAO


class FacultyDAO(BaseDAO):

    def get_model(self):
        return Faculty

    def get_Unique(self):
        return None
