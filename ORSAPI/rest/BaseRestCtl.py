import logging
from abc import ABC, abstractmethod
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


class BaseRestCtl(APIView, ABC):
    """Abstract base class inherited by all REST API controllers."""

    @abstractmethod
    def get_model(self):
        """Return the Django model class for this controller."""
        pass

    @abstractmethod
    def get_service(self):
        """Return the Django service class for this controller."""
        pass

    def input_validation(self, _data):
        """Perform manual field validation on request data. Return a dict of {field: error} or {}."""
        return {}

    @abstractmethod
    def get_serializer_class(self):
        """Return the DRF serializer class for this controller."""
        pass

    def get_resource_name(self):
        """Return a display name used in response messages; defaults to the model class name."""
        return self.get_model().__name__

    # --- Response helpers ---

    def success_response(self, data=None, message="", stcode=status.HTTP_200_OK):
        res_data = {
            "error": False,
            "message": message,
            "data": data,
        }
        return Response(res_data, status=stcode)

    def error_response(
        self, errors=None, message="", stcode=status.HTTP_400_BAD_REQUEST
    ):
        res_data = {
            "error": True,
            "message": message,
            "errors": errors,
        }
        return Response(res_data, status=stcode)

    # --- Default CRUD implementations ---

    def get(self, request, id=None):
        """Return a single record by id, or a (optionally filtered) list when id is omitted.

        When id is omitted and the request carries a JSON body, each key/value
        pair is forwarded to service.search() so the caller can narrow results
        without a dedicated search endpoint.
        """
        logger.info("%s.get() id=%s", self.__class__.__name__, id)
        service = self.get_service()()
        serializer_class = self.get_serializer_class()
        if id:
            obj = service.get(id)
            if obj is None:
                return self.error_response(
                    None, "Object not found", status.HTTP_404_NOT_FOUND
                )
            return self.success_response(serializer_class(obj).data)

        print("request.data:", request.data)
        filters = request.data if isinstance(request.data, dict) else {}
        if filters:
            logger.info(
                "%s.get() applying filters=%s", self.__class__.__name__, filters
            )
        queryset = service.search(filters)
        return self.success_response(serializer_class(queryset, many=True).data)

    @classmethod
    def search_view(cls):
        """Return an as_view() entry where POST routes to search() instead of create."""
        class _SearchView(cls):
            def post(self, request, *args, **kwargs):
                return self.search(request)

        _SearchView.__name__ = f"{cls.__name__}SearchView"
        return _SearchView.as_view()

    def search(self, request):
        filters = request.data if isinstance(request.data, dict) else {}
        if filters:
            logger.info(
                "%s.search() applying filters=%s", self.__class__.__name__, filters
            )
        queryset = self.get_service()().search(filters)
        return self.success_response(
            self.get_serializer_class()(queryset, many=True).data
        )

    def post(self, request):
        """Validate and create a new record; return 201 on success or 400 on validation failure."""
        logger.info("%s.post()", self.__class__.__name__)
        errors = self.input_validation(request.data)
        if errors:
            return self.error_response(errors, "Validation failed")

        obj = self.get_model()(**request.data)
        self.get_service()().save(obj)
        msg = f"{self.get_resource_name()} saved successfully"
        return self.success_response(
            self.get_serializer_class()(obj).data,
            msg,
            status.HTTP_201_CREATED,
        )

    def put(self, request, id):
        """Validate and update an existing record by id; return 404 if not found or 400 on validation failure."""
        logger.info("%s.put() id=%s", self.__class__.__name__, id)
        service = self.get_service()()
        obj = service.get(id)
        if obj is None:
            msg = f"{self.get_resource_name()} not found"
            return self.error_response(None, msg, status.HTTP_404_NOT_FOUND)

        errors = self.input_validation(request.data)
        if errors:
            return self.error_response(errors, "Validation failed")

        for field, value in request.data.items():
            setattr(obj, field, value)
        service.save(obj)
        msg = f"{self.get_resource_name()} updated successfully"
        return self.success_response(self.get_serializer_class()(obj).data, msg)

    def delete(self, request, id):
        """Delete a record by id; return 404 if not found."""
        logger.info("%s.delete() id=%s", self.__class__.__name__, id)
        service = self.get_service()()
        obj = service.get(id)
        if obj is None:
            msg = f"{self.get_resource_name()} not found"
            return self.error_response(None, msg, status.HTTP_404_NOT_FOUND)
        service.delete(id)
        msg = f"{self.get_resource_name()} deleted successfully"
        return self.success_response(None, msg)
