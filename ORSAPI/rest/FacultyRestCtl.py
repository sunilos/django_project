from rest_framework.response import Response
from rest_framework.views import APIView
from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Faculty, College, Course, Subject
from service.Serializers import FacultySerializers
from service.service.FacultyService import FacultyService
from service.utility.DataValidator import DataValidator


class FacultyRestCtl(BaseRestCtl):
    def get_model(self):
        return Faculty

    def get_service(self):
        return FacultyService

    def get_serializer_class(self):
        return FacultySerializers

    def input_validation(self, data):
        errors = {}

        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        email = data.get("email", "")
        mobile = data.get("mobileNumber", "")
        gender = data.get("gender", "")

        if DataValidator.isNull(first_name):
            errors["firstName"] = "First Name cannot be null"
        elif not DataValidator.isMaxLength(first_name, 50):
            errors["firstName"] = "First Name cannot exceed 50 characters"

        if DataValidator.isNull(last_name):
            errors["lastName"] = "Last Name cannot be null"
        elif not DataValidator.isMaxLength(last_name, 50):
            errors["lastName"] = "Last Name cannot exceed 50 characters"

        if DataValidator.isNull(email):
            errors["email"] = "Email cannot be null"
        elif not DataValidator.isEmail(email):
            errors["email"] = "Email must be a valid email address"

        if DataValidator.isNull(mobile):
            errors["mobileNumber"] = "Mobile Number cannot be null"
        elif not DataValidator.isDigit(mobile):
            errors["mobileNumber"] = "Mobile Number must contain digits only"
        elif not DataValidator.isMaxLength(mobile, 20):
            errors["mobileNumber"] = "Mobile Number cannot exceed 20 characters"

        if DataValidator.isNull(gender):
            errors["gender"] = "Gender cannot be null"

        return errors


class FacultyPreloadRestCtl(APIView):
    def get(self, _request):
        data = {
            "colleges": [
                {"id": c.get_key(), "value": c.get_value()}
                for c in College.objects.order_by("name")
            ],
            "courses": [
                {"id": c.get_key(), "value": c.get_value()}
                for c in Course.objects.order_by("name")
            ],
            "subjects": [
                {"id": c.get_key(), "value": c.get_value()}
                for c in Subject.objects.order_by("subjectName")
            ],
        }
        return Response({"error": False, "message": "", "data": data})
