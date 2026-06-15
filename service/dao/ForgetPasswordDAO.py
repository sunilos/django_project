from service.models import User
from .BaseDAO import BaseDAO


class ForgetPasswordDAO(BaseDAO):

    def get_model(self):
        return User

    def get_Unique(self):
        return ["login"]
