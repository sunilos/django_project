from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Course
from service.Serializers import CourseSerializers
from service.service.CourseService import CourseService
from service.utility.DataValidator import DataValidator


class CourseRestCtl(BaseRestCtl):
    def get_model(self):
        return Course

    def get_service(self):
        return CourseService

    def get_serializer_class(self):
        return CourseSerializers

    def input_validation(self, data):
        errors = {}

        name = data.get("name", "")
        description = data.get("description", "")
        duration = data.get("duration", "")

        if DataValidator.isNull(name):
            errors["name"] = "Name cannot be null"
        elif not DataValidator.isMaxLength(name, 50):
            errors["name"] = "Name cannot exceed 50 characters"

        if DataValidator.isNull(description):
            errors["description"] = "Description cannot be null"
        elif not DataValidator.isMaxLength(description, 100):
            errors["description"] = "Description cannot exceed 100 characters"

        if DataValidator.isNull(duration):
            errors["duration"] = "Duration cannot be null"
        elif not DataValidator.isMaxLength(duration, 100):
            errors["duration"] = "Duration cannot exceed 100 characters"

        return errors
