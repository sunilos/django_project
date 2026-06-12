from service.models import TimeTable
from .BaseDAO import BaseDAO


class TimeTableDAO(BaseDAO):

    def get_model(self):
        return TimeTable
