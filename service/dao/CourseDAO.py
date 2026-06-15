from service.models import Course
from .BaseDAO import BaseDAO


class CourseDAO(BaseDAO):

    def get_model(self):
        return Course

    def get_Unique(self):
        return ["name"]
