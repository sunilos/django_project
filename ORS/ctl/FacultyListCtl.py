from django.shortcuts import render

from service.service.SubjectService import SubjectService
from .BaseCtl import BaseCtl
from service.service.FacultyService import FacultyService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from ORS.utility.HtmlUtility import HtmlUtility


class FacultyListCtl(BaseCtl):

    def preload(self, request):
        college_list = CollegeService().search({})
        course_list = CourseService().search({})
        subject_list = SubjectService().search({})
        self.preload_data["college_select"] = HtmlUtility.get_list_from_beans(
            "college_ID",
            int(self.form.get("college_ID") or 0),
            college_list,
        )
        self.preload_data["course_select"] = HtmlUtility.get_list_from_beans(
            "course_ID",
            int(self.form.get("course_ID") or 0),
            course_list,
        )
        self.preload_data["subject_select"] = HtmlUtility.get_list_from_beans(
            "subject_ID",
            int(self.form.get("subject_ID") or 0),
            subject_list,
        )
        return self.preload_data

    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName", None)
        self.form["lastName"] = requestForm.get("lastName", None)
        self.form["email"] = requestForm.get("email", None)
        self.form["college_ID"] = requestForm.get("college_ID", None)
        self.form["course_ID"] = requestForm.get("course_ID", None)
        self.form["subject_ID"] = requestForm.get("subject_ID", None)
        self.form["page_number"] = int(requestForm.get("page_number", 1) or 1)

    def display(self, request, params={}):
        page_list = self.get_service().search(self.form, page_number=1)
        return render(
            request,
            self.get_template(),
            {"pageList": page_list, "form": self.form, "preload_data": self.preload(request)},
        )

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        page_number = int(self.form.get("page_number", 1))
        page_list = self.get_service().search(self.form, page_number=page_number)
        return render(
            request,
            self.get_template(),
            {
                "pageList": page_list,
                "form": self.form,
                "preload_data": self.preload(request),
            },
        )

    def get_template(self):
        return "ors/FacultyList.html"

    def get_service(self):
        return FacultyService()
