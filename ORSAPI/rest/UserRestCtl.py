import os
import uuid
from datetime import datetime

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from ORSAPI.rest.BaseRestCtl import BaseRestCtl
from service.models import User, Role
from service.Serializers import UserSerializers
from service.service.UserService import UserService
from service.service.ForgetPasswordService import ForgetPasswordService
from service.mail.EmailService import EmailService
from service.mail.EmailBuilder import EmailBuilder
from service.mail.EmailMessage import EmailMessage
from service.utility.DataValidator import DataValidator


class UserRestCtl(BaseRestCtl):
    def get_model(self):
        return User

    def get_service(self):
        return UserService()

    def get_serializer_class(self):
        return UserSerializers

    def input_validation(self, data):
        errors = {}

        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        login = data.get("login", "")
        password = data.get("password", "")
        mobile = data.get("mobileNumber", "")
        role_id = data.get("role_id", "")

        if DataValidator.isNull(first_name):
            errors["firstName"] = "First Name cannot be null"
        elif not DataValidator.isMaxLength(first_name, 50):
            errors["firstName"] = "First Name cannot exceed 50 characters"

        if DataValidator.isNull(last_name):
            errors["lastName"] = "Last Name cannot be null"
        elif not DataValidator.isMaxLength(last_name, 50):
            errors["lastName"] = "Last Name cannot exceed 50 characters"

        if DataValidator.isNull(login):
            errors["login"] = "Login cannot be null"
        elif not DataValidator.isEmail(login):
            errors["login"] = "Login must be a valid email address"

        if DataValidator.isNull(password):
            errors["password"] = "Password cannot be null"
        elif not DataValidator.isMaxLength(password, 20):
            errors["password"] = "Password cannot exceed 20 characters"

        if DataValidator.isNull(mobile):
            errors["mobileNumber"] = "Mobile Number cannot be null"
        elif not DataValidator.isDigit(mobile):
            errors["mobileNumber"] = "Mobile Number must contain digits only"
        elif not DataValidator.isMaxLength(mobile, 15):
            errors["mobileNumber"] = "Mobile Number cannot exceed 15 characters"

        if DataValidator.isNull(role_id):
            errors["role_id"] = "Role cannot be null"
        elif not DataValidator.isInteger(role_id):
            errors["role_id"] = "Role ID must be a valid integer"
        elif int(role_id) <= 0:
            errors["role_id"] = "Role ID must be a positive integer"

        return errors


class UserLoginRestCtl(BaseRestCtl):
    """
    REST endpoint for user authentication.

    POST /ORSAPI/api/User/login/

    Request body:
        {
            "login": "user@example.com",
            "password": "yourpassword"
        }

    Responses:
        200 - Valid credentials   : {"error": false, "message": "Login successful", "data": {"user": {...}, "access": "...", "refresh": "..."}}
        400 - Missing fields      : {"error": true,  "message": "Login and password are required"}
        401 - Wrong credentials   : {"error": true,  "message": "Invalid login or password"}
    """

    permission_classes = [AllowAny]

    def get_model(self):
        return User

    def get_service(self):
        return UserService()

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        loginId = request.data.get("loginId", "")

        password = request.data.get("password", "")
        print("Login attempt for:", loginId, password)  # Debug log

        if not loginId or not password:
            return self.error_response(None, "Login and password are required", status.HTTP_400_BAD_REQUEST)

        user = UserService().authenticate({"loginId": loginId, "password": password})
        if user is None:
            return self.error_response(None, "Invalid login or password", status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken()
        refresh["user_id"] = user.id
        refresh["login"] = user.login
        refresh["role_id"] = user.role_id

        return Response({
            "error": False,
            "message": "Login successful",
            "data": {
                "user": UserSerializers(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
        })


class ChangePasswordRestCtl(BaseRestCtl):
    """
    REST endpoint to change a user's password.

    POST /ORSAPI/api/User/change-password/

    Request body:
        {
            "login": "user@example.com",
            "oldPassword": "current",
            "newPassword": "newpass",
            "confirmPassword": "newpass"
        }

    Responses:
        200 - Success      : {"error": false, "message": "Password changed successfully"}
        400 - Validation   : {"error": true,  "message": "...", "errors": {...}}
        404 - User missing : {"error": true,  "message": "User not found"}
    """

    def get_model(self):
        return User

    def get_service(self):
        return UserService()

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        login = request.data.get("login", "")
        old_password = request.data.get("oldPassword", "")
        new_password = request.data.get("newPassword", "")
        confirm_password = request.data.get("confirmPassword", "")

        errors = {}
        if not login:
            errors["login"] = "Login cannot be null"
        if not old_password:
            errors["oldPassword"] = "Old Password cannot be null"
        if not new_password:
            errors["newPassword"] = "New Password cannot be null"
        if not confirm_password:
            errors["confirmPassword"] = "Confirm Password cannot be null"
        elif new_password and new_password != confirm_password:
            errors["confirmPassword"] = "New Password and Confirm Password do not match"
        if errors:
            return self.error_response(errors, "Validation failed", status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            return self.error_response(None, "User not found", status.HTTP_404_NOT_FOUND)

        if user.password != old_password:
            return self.error_response({"oldPassword": "Old Password is incorrect"}, "Validation failed", status.HTTP_400_BAD_REQUEST)

        user.password = new_password
        UserService().save(user)

        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Password Changed Successfully"
        msg.text = EmailBuilder.change_password({"firstName": user.firstName, "login": user.login, "password": new_password})
        EmailService.send(msg)

        return self.error_response(None, "Password changed successfully", status.HTTP_200_OK)


class ForgotPasswordRestCtl(BaseRestCtl):
    """
    REST endpoint to trigger a forgot-password email.

    POST /ORSAPI/api/User/forgot-password/

    Request body:
        {
            "login": "user@example.com"
        }

    Responses:
        200 - Email sent   : {"error": false, "message": "Password reset email has been sent"}
        400 - Missing login: {"error": true,  "message": "Login cannot be null"}
        404 - Not found    : {"error": true,  "message": "No account found with this email"}
    """

    permission_classes = [AllowAny]

    def get_model(self):
        return User

    def get_service(self):
        return ForgetPasswordService()

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        loginId = request.data.get("login", "")

        if not loginId:
            return self.error_response(None, "Login cannot be null", status.HTTP_400_BAD_REQUEST)

        user_qs = ForgetPasswordService().search({"login": loginId})
        if user_qs.count() == 0:
            return self.error_response(None, "No account found with this email", status.HTTP_404_NOT_FOUND)

        user = user_qs[0]
        msg = EmailMessage()
        msg.to = [user.login]
        msg.subject = "Forgot Password Request"
        msg.text = EmailBuilder.forgot_password({"firstName": user.firstName, "login": user.login, "password": user.password})
        EmailService.send(msg)

        return self.error_response(None, "Password reset email has been sent", status.HTTP_200_OK)


class UserRegistrationRestCtl(BaseRestCtl):
    """
    REST endpoint for new user self-registration.

    POST /ORSAPI/api/User/register/

    Request body:
        {
            "firstName": "John",
            "lastName":  "Doe",
            "login":     "john@example.com",
            "password":  "secret",
            "mobileNumber": "9876543210",
            "gender":    "Male",
            "dob":       "1990-01-25"   (optional, YYYY-MM-DD)
        }

    Responses:
        201 - Registered   : {"error": false, "message": "Registration successful", "data": {...user}}
        400 - Validation   : {"error": true,  "message": "Validation failed", "errors": {...}}
    """

    permission_classes = [AllowAny]

    def get_model(self):
        return User

    def get_service(self):
        return UserService()

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        data = request.data
        errors = {}

        first_name = data.get("firstName", "")
        last_name = data.get("lastName", "")
        loginId = data.get("login", "")
        password = data.get("password", "")
        mobile = data.get("mobileNumber", "")
        gender = data.get("gender", "Male")
        dob = data.get("dob", "")

        if not first_name:
            errors["firstName"] = "First Name cannot be null"
        if not last_name:
            errors["lastName"] = "Last Name cannot be null"
        if not loginId:
            errors["login"] = "Login cannot be null"
        elif "@" not in loginId or "." not in loginId:
            errors["login"] = "Login must be a valid email address"
        elif User.objects.filter(login=loginId).exists():
            errors["login"] = "This email is already registered"
        if not password:
            errors["password"] = "Password cannot be null"
        if not mobile:
            errors["mobileNumber"] = "Mobile Number cannot be null"
        elif not mobile.isdigit() or len(mobile) != 10:
            errors["mobileNumber"] = "Mobile Number must be 10 digits"
        if errors:
            return self.error_response(errors, "Validation failed", status.HTTP_400_BAD_REQUEST)

        user = User()
        user.firstName = first_name
        user.lastName = last_name
        user.login = loginId
        user.password = password
        user.mobileNumber = mobile
        user.gender = gender
        user.role_id = 2
        user.role_Name = ""
        user.dob = datetime.strptime(dob, "%Y-%m-%d").date() if dob else None
        UserService().save(user)

        msg = EmailMessage()
        msg.to = [loginId]
        msg.subject = "Welcome - Registration Successful"
        msg.text = EmailBuilder.sign_up({"firstName": first_name, "login": loginId, "password": password})
        EmailService.send(msg)

        return self.success_response(UserSerializers(user).data, "Registration successful", status.HTTP_201_CREATED)


class UserPreloadRestCtl(APIView):
    def get(self, _request):
        data = {
            "roles": [{"id": r.get_key(), "value": r.get_value()} for r in Role.objects.order_by("name")],
        }
        return Response({"error": False, "message": "", "data": data})


class UploadUserPhotoRestCtl(BaseRestCtl):
    """
    REST endpoint to upload a user profile photo.

    POST /ORSAPI/api/User/upload-photo/

    Request: multipart/form-data
        user_id  — ID of the user whose photo is being uploaded
        photo    — image file

    Responses:
        200 - Success   : {"error": false, "message": "Photo uploaded successfully", "data": {...user}}
        400 - Validation: {"error": true,  "message": "...", "errors": {...}}
        404 - Not found : {"error": true,  "message": "User not found"}
    """

    def get_model(self):
        return User

    def get_service(self):
        return UserService()

    def get_serializer_class(self):
        return UserSerializers

    def post(self, request):
        user_id = request.data.get("user_id", "")
        photo_file = request.FILES.get("photo")

        errors = {}
        if not user_id:
            errors["user_id"] = "User ID cannot be null"
        if not photo_file:
            errors["photo"] = "Photo file cannot be null"
        if errors:
            return self.error_response(errors, "Validation failed", status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=int(user_id))
        except (User.DoesNotExist, ValueError):
            return self.error_response(None, "User not found", status.HTTP_404_NOT_FOUND)

        ext = os.path.splitext(photo_file.name)[1].lower()
        filename = f"user_{uuid.uuid4().hex}{ext}"
        dest_dir = os.path.join(settings.MEDIA_ROOT, settings.USER_PHOTO_DIR)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, filename)
        with open(dest_path, "wb+") as f:
            for chunk in photo_file.chunks():
                f.write(chunk)

        user.photo = f"{settings.USER_PHOTO_DIR}/{filename}"
        UserService().save(user)

        return self.success_response(UserSerializers(user).data, "Photo uploaded successfully")
