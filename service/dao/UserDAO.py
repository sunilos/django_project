from service.models import User
from .BaseDAO import BaseDAO


class UserDAO(BaseDAO):

    def get_by_login(self, login):
        try:
            return self.get_model().objects.get(login=login)
        except self.get_model().DoesNotExist:
            return None

    def get_model(self):
        return User
