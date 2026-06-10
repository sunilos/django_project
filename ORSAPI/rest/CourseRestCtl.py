from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Course
from service.Serializers import CourseSerializers
from service.service.CourseService import CourseService


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

        if not name:
            errors["name"] = "Name cannot be null"
        elif len(name) > 50:
            errors["name"] = "Name cannot exceed 50 characters"

        if not description:
            errors["description"] = "Description cannot be null"
        elif len(description) > 100:
            errors["description"] = "Description cannot exceed 100 characters"

        if not duration:
            errors["duration"] = "Duration cannot be null"
        elif len(duration) > 100:
            errors["duration"] = "Duration cannot exceed 100 characters"

        return errors
