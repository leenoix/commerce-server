from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
from django.views import View

from commerce.utils.json import CommerceEncoder


class JsonView(View):
    REQUIRED_FIELDS = {}

    LOGIN_REQUIRED = False

    def is_valid_request(self, request):
        pass

    @staticmethod
    def has_all_fields(request, required):
        return all([f in request for f in required])

    @staticmethod
    def catch_invalid_fields(request, required):
        pass

    def get_missing_fields(self, request):
        data = getattr(request, request.method, [])

        if isinstance(self.REQUIRED_FIELDS, dict):
            required_fields = self.REQUIRED_FIELDS.get(request.method)
        else:
            required_fields = self.REQUIRED_FIELDS

        if not required_fields:
            return []

        if not all([v in data for v in required_fields]):
            return list(set(required_fields).difference(data))

        return []

    def dispatch(self, request, *args, **kwargs):
        missing_fields = self.get_missing_fields(request)
        if missing_fields:
            return JsonResponse(dict(code='MISSING_ELEMENTS', msg='Missing elements', elements=missing_fields), status=422)

        if self.LOGIN_REQUIRED and not request.user.is_authenticated:
            return JsonResponse(dict(code='UNAUTHORIZED'), status=401)

        if self.LOGIN_REQUIRED and request.user.deleted_at:
            logout(request)
            return JsonResponse(dict(code='UNAUTHORIZED'), status=401)

        response = super().dispatch(request, *args, **kwargs)
        if isinstance(response, HttpResponse):
            return response
        if isinstance(response, tuple):
            return JsonResponse(response[0], encoder=CommerceEncoder, status=response[1])
        if isinstance(response, dict):
            return JsonResponse(response, encoder=CommerceEncoder)
        if isinstance(response, list):
            return JsonResponse(response, encoder=CommerceEncoder, safe=False)
        raise TypeError

