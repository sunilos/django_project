from service.models import Marksheet
from .BaseDAO import BaseDAO


class MarksheetDAO(BaseDAO):

    def get_model(self):
        return Marksheet

    def get_Unique(self):
        return ["rollNumber"]
