from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Role
from service.Serializers import RoleSerializers
from service.service.RoleService import RoleService
from service.utility.DataValidator import DataValidator


class RoleRestCtl(BaseRestCtl):
    def get_model(self):
        return Role

    def get_service(self):
        return RoleService()

    def get_serializer_class(self):
        return RoleSerializers

    def input_validation(self, data):
        errors = {}

        name = data.get("name", "")
        description = data.get("description", "")

        if DataValidator.isNull(name):
            errors["name"] = "Name cannot be null"
        elif not DataValidator.isMaxLength(name, 100):
            errors["name"] = "Name cannot exceed 100 characters"

        if DataValidator.isNull(description):
            errors["description"] = "Description cannot be null"
        elif not DataValidator.isMaxLength(description, 500):
            errors["description"] = "Description cannot exceed 500 characters"

        return errors
