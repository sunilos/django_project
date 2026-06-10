from rest_framework.response import Response
from rest_framework.views import APIView
from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Student, College
from service.Serializers import StudentSerializers
from service.service.StudentService import StudentService


class StudentRestCtl(BaseRestCtl):
    def get_model(self):
        return Student

    def get_service(self):
        return StudentService

    def get_serializer_class(self):
        return StudentSerializers

    def input_validation(self, data):
        errors = {}

        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        mobile = data.get("mobileNumber", "")
        email = data.get("email", "")
        college_id = data.get("college_ID", "")

        if not first_name:
            errors["firstName"] = "First Name cannot be null"
        elif len(first_name) > 50:
            errors["firstName"] = "First Name cannot exceed 50 characters"

        if not last_name:
            errors["lastName"] = "Last Name cannot be null"
        elif len(last_name) > 50:
            errors["lastName"] = "Last Name cannot exceed 50 characters"

        if not mobile:
            errors["mobileNumber"] = "Mobile Number cannot be null"
        elif not str(mobile).isdigit():
            errors["mobileNumber"] = "Mobile Number must contain digits only"
        elif len(str(mobile)) > 20:
            errors["mobileNumber"] = "Mobile Number cannot exceed 20 characters"

        if not email:
            errors["email"] = "Email cannot be null"
        elif "@" not in email or "." not in email:
            errors["email"] = "Email must be a valid email address"

        if not college_id:
            errors["college_ID"] = "College cannot be null"
        else:
            try:
                if int(college_id) <= 0:
                    errors["college_ID"] = "College ID must be a positive integer"
            except (ValueError, TypeError):
                errors["college_ID"] = "College ID must be a valid integer"

        return errors


class StudentPreloadRestCtl(APIView):
    def get(self, _request):
        colleges = [{"id": c.get_key(), "value": c.get_value()} for c in College.objects.order_by("name")]
        data = {"colleges": colleges}
        return Response({"error": False, "message": "", "data": data})
