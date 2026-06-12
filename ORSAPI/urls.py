"""SOSWebProjects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .rest.CollegeRestCtl import CollegeRestCtl
from .rest.StudentRestCtl import StudentPreloadRestCtl, StudentRestCtl
from .rest.CourseRestCtl import CourseRestCtl
from .rest.FacultyRestCtl import FacultyRestCtl, FacultyPreloadRestCtl
from .rest.RoleRestCtl import RoleRestCtl
from .rest.MarksheetRestCtl import MarksheetRestCtl
from .rest.SubjectRestCtl import SubjectRestCtl, SubjectPreloadRestCtl
from .rest.UserRestCtl import (
    UserRestCtl,
    UserLoginRestCtl,
    ChangePasswordRestCtl,
    ForgotPasswordRestCtl,
    UserRegistrationRestCtl,
    UserPreloadRestCtl,
)

urlpatterns = [
    path("api/token/refresh/", TokenRefreshView.as_view()),
    # REST API routes — must be before the generic catch-all patterns
    path("api/College/", CollegeRestCtl.as_view()),
    path("api/College/search/", CollegeRestCtl.search_view(), name="college-search"),
    path("api/College/<int:id>/", CollegeRestCtl.as_view()),
    path("api/Student/", StudentRestCtl.as_view()),
    path("api/Student/search/", StudentRestCtl.search_view(), name="student-search"),
    path("api/Student/<int:id>/", StudentRestCtl.as_view()),
    path("api/Student/preload/", StudentPreloadRestCtl.as_view()),
    path("api/Course/", CourseRestCtl.as_view()),
    path("api/Course/search/", CourseRestCtl.search_view(), name="course-search"),
    path("api/Course/<int:id>/", CourseRestCtl.as_view()),
    path("api/Faculty/", FacultyRestCtl.as_view()),
    path("api/Faculty/search/", FacultyRestCtl.search_view(), name="faculty-search"),
    path("api/Faculty/<int:id>/", FacultyRestCtl.as_view()),
    path("api/Faculty/preload/", FacultyPreloadRestCtl.as_view()),
    path("api/Role/", RoleRestCtl.as_view()),
    path("api/Role/search/", RoleRestCtl.search_view(), name="role-search"),
    path("api/Role/<int:id>/", RoleRestCtl.as_view()),
    path("api/Marksheet/", MarksheetRestCtl.as_view()),
    path("api/Marksheet/search/", MarksheetRestCtl.search_view(), name="marksheet-search"),
    path("api/Marksheet/<int:id>/", MarksheetRestCtl.as_view()),
    path("api/Subject/", SubjectRestCtl.as_view()),
    path("api/Subject/search/", SubjectRestCtl.search_view(), name="subject-search"),
    path("api/Subject/<int:id>/", SubjectRestCtl.as_view()),
    path("api/Subject/preload/", SubjectPreloadRestCtl.as_view()),
    path("api/User/", UserRestCtl.as_view()),
    path("api/User/search/", UserRestCtl.search_view(), name="user-search"),
    path("api/User/<int:id>/", UserRestCtl.as_view()),
    path("api/User/preload/", UserPreloadRestCtl.as_view()),
    path("api/User/login/", UserLoginRestCtl.as_view()),
    path("api/User/change-password/", ChangePasswordRestCtl.as_view()),
    path("api/User/forgot-password/", ForgotPasswordRestCtl.as_view()),
    path("api/User/register/", UserRegistrationRestCtl.as_view()),
]
