from rest_framework.response import Response
from rest_framework.views import APIView
from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Subject, Course
from service.Serializers import SubjectSerializers
from service.service.SubjectService import SubjectService


class SubjectRestCtl(BaseRestCtl):
    def get_model(self):
        return Subject

    def get_service(self):
        return SubjectService

    def get_serializer_class(self):
        return SubjectSerializers

    def input_validation(self, data):
        errors = {}

        subject_name = data.get("subjectName", "")
        subject_desc = data.get("subjectDescription", "")
        course_id = data.get("course_ID", "")

        if not subject_name:
            errors["subjectName"] = "Subject Name cannot be null"
        elif len(subject_name) > 50:
            errors["subjectName"] = "Subject Name cannot exceed 50 characters"

        if not subject_desc:
            errors["subjectDescription"] = "Subject Description cannot be null"
        elif len(subject_desc) > 200:
            errors["subjectDescription"] = "Subject Description cannot exceed 200 characters"

        if not course_id:
            errors["course_ID"] = "Course cannot be null"
        else:
            try:
                if int(course_id) <= 0:
                    errors["course_ID"] = "Course ID must be a positive integer"
            except (ValueError, TypeError):
                errors["course_ID"] = "Course ID must be a valid integer"

        return errors


class SubjectPreloadRestCtl(APIView):
    def get(self, _request):
        courses = [{"id": c.get_key(), "value": c.get_value()} for c in Course.objects.order_by("name")]
        data = {"courses": courses}
        return Response({"error": False, "message": "", "data": data})
