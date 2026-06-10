from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import Marksheet
from service.Serializers import MarksheetSerializers
from service.service.MarksheetService import MarksheetService
from service.utility.DataValidator import DataValidator


class MarksheetRestCtl(BaseRestCtl):
    def get_model(self):
        return Marksheet

    def get_service(self):
        return MarksheetService

    def get_serializer_class(self):
        return MarksheetSerializers

    def input_validation(self, data):
        errors = {}

        roll_number = data.get("rollNumber", "")
        name = data.get("name", "")
        physics = data.get("physics")
        chemistry = data.get("chemistry")
        maths = data.get("maths")
        year = data.get("year")
        student_id = data.get("student_id", "")

        if DataValidator.isNull(roll_number):
            errors["rollNumber"] = "Roll Number cannot be null"
        elif not DataValidator.isMaxLength(roll_number, 50):
            errors["rollNumber"] = "Roll Number cannot exceed 50 characters"

        if DataValidator.isNull(name):
            errors["name"] = "Name cannot be null"
        elif not DataValidator.isMaxLength(name, 50):
            errors["name"] = "Name cannot exceed 50 characters"

        for field, value in (("physics", physics), ("chemistry", chemistry), ("maths", maths)):
            if DataValidator.isNull(value):
                errors[field] = f"{field.capitalize()} marks cannot be null"
            elif not DataValidator.isRange(value, 0, 100):
                errors[field] = f"{field.capitalize()} marks must be between 0 and 100"

        if DataValidator.isNull(year):
            errors["year"] = "Year cannot be null"
        elif not DataValidator.isRange(year, 1900, 2100):
            errors["year"] = "Year must be between 1900 and 2100"

        if DataValidator.isNull(student_id):
            errors["student_id"] = "Student cannot be null"
        elif not DataValidator.isInteger(student_id):
            errors["student_id"] = "Student ID must be a valid integer"
        elif int(student_id) <= 0:
            errors["student_id"] = "Student ID must be a positive integer"

        return errors

    def get(self, request, id=None):
        if id:
            try:
                obj = Marksheet.objects.get(id=id)
            except Marksheet.DoesNotExist:
                return self.error_response(None, "Marksheet not found", status.HTTP_404_NOT_FOUND)
            data = dict(MarksheetSerializers(obj).data)
            data["total"] = obj.total
            data["percentage"] = obj.percentage
        else:
            objs = Marksheet.objects.all()
            data = []
            for obj, item in zip(objs, MarksheetSerializers(objs, many=True).data):
                entry = dict(item)
                entry["total"] = obj.total
                entry["percentage"] = obj.percentage
                data.append(entry)
        return self.success_response(True, data,status=200)
