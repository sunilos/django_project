from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import College
from service.Serializers import CollegeSerializers
from service.service.CollegeService import CollegeService
from service.utility.DataValidator import DataValidator


class CollegeRestCtl(BaseRestCtl):
    def get_model(self):
        return College

    def get_service(self):
        return CollegeService()

    def get_serializer_class(self):
        return CollegeSerializers

    def input_validation(self, data):
        errors = {}

        name = data.get("name", "")
        address = data.get("address", "")
        state = data.get("state", "")
        city = data.get("city", "")
        phone = data.get("phoneNumber", "")

        if DataValidator.isNull(name):
            errors["name"] = "Name cannot be null"
        elif not DataValidator.isMaxLength(name, 50):
            errors["name"] = "Name cannot exceed 50 characters"

        if DataValidator.isNull(address):
            errors["address"] = "Address cannot be null"
        elif not DataValidator.isMaxLength(address, 50):
            errors["address"] = "Address cannot exceed 50 characters"

        if DataValidator.isNull(state):
            errors["state"] = "State cannot be null"
        elif not DataValidator.isMaxLength(state, 50):
            errors["state"] = "State cannot exceed 50 characters"

        if DataValidator.isNull(city):
            errors["city"] = "City cannot be null"
        elif not DataValidator.isMaxLength(city, 20):
            errors["city"] = "City cannot exceed 20 characters"

        if DataValidator.isNull(phone):
            errors["phoneNumber"] = "Phone Number cannot be null"
        elif not DataValidator.isDigit(phone):
            errors["phoneNumber"] = "Phone Number must contain digits only"
        elif not DataValidator.isMaxLength(phone, 20):
            errors["phoneNumber"] = "Phone Number cannot exceed 20 characters"

        return errors
