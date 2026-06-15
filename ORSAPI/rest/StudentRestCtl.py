from rest_framework.response import Response
from rest_framework.views import APIView
from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Student, College
from service.Serializers import StudentSerializers
from service.service.StudentService import StudentService
from service.utility.DataValidator import DataValidator


class StudentRestCtl(BaseRestCtl):
    def get_model(self):
        return Student

    def get_service(self):
        return StudentService()

    def get_serializer_class(self):
        return StudentSerializers

    def input_validation(self, data):
        errors = {}

        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        mobile = data.get("mobileNumber", "")
        email = data.get("email", "")
        college_id = data.get("college_ID", "")

        if DataValidator.isNull(first_name):
            errors["firstName"] = "First Name cannot be null"
        elif not DataValidator.isMaxLength(first_name, 50):
            errors["firstName"] = "First Name cannot exceed 50 characters"

        if DataValidator.isNull(last_name):
            errors["lastName"] = "Last Name cannot be null"
        elif not DataValidator.isMaxLength(last_name, 50):
            errors["lastName"] = "Last Name cannot exceed 50 characters"

        if DataValidator.isNull(mobile):
            errors["mobileNumber"] = "Mobile Number cannot be null"
        elif not DataValidator.isDigit(mobile):
            errors["mobileNumber"] = "Mobile Number must contain digits only"
        elif not DataValidator.isMaxLength(mobile, 20):
            errors["mobileNumber"] = "Mobile Number cannot exceed 20 characters"

        if DataValidator.isNull(email):
            errors["email"] = "Email cannot be null"
        elif not DataValidator.isEmail(email):
            errors["email"] = "Email must be a valid email address"

        if DataValidator.isNull(college_id):
            errors["college_ID"] = "College cannot be null"
        elif not DataValidator.isInteger(college_id):
            errors["college_ID"] = "College ID must be a valid integer"
        elif int(college_id) <= 0:
            errors["college_ID"] = "College ID must be a positive integer"

        return errors


class StudentPreloadRestCtl(APIView):
    def get(self, _request):
        colleges = [{"id": c.get_key(), "value": c.get_value()} for c in College.objects.order_by("name")]
        data = {"colleges": colleges}
        return Response({"error": False, "message": "", "data": data})
