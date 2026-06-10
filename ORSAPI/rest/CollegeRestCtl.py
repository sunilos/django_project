from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import College
from service.Serializers import CollegeSerializers
from service.service.CollegeService import CollegeService


class CollegeRestCtl(BaseRestCtl):
    def get_model(self):
        return College

    def get_service(self):
        return CollegeService

    def get_serializer_class(self):
        return CollegeSerializers

    def input_validation(self, data):
        errors = {}

        name = data.get("name", "")
        address = data.get("address", "")
        state = data.get("state", "")
        city = data.get("city", "")
        phone = data.get("phoneNumber", "")

        if not name:
            errors["name"] = "Name cannot be null"
        elif len(name) > 50:
            errors["name"] = "Name cannot exceed 50 characters"

        if not address:
            errors["address"] = "Address cannot be null"
        elif len(address) > 50:
            errors["address"] = "Address cannot exceed 50 characters"

        if not state:
            errors["state"] = "State cannot be null"
        elif len(state) > 50:
            errors["state"] = "State cannot exceed 50 characters"

        if not city:
            errors["city"] = "City cannot be null"
        elif len(city) > 20:
            errors["city"] = "City cannot exceed 20 characters"

        if not phone:
            errors["phoneNumber"] = "Phone Number cannot be null"
        elif not phone.isdigit():
            errors["phoneNumber"] = "Phone Number must contain digits only"
        elif len(phone) > 20:
            errors["phoneNumber"] = "Phone Number cannot exceed 20 characters"

        return errors
