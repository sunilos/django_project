from service.models import Role
from .BaseDAO import BaseDAO


class RoleDAO(BaseDAO):

    def get_model(self):
        return Role
