import json

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseBadRequest


class JSONParsingMiddleware(MiddlewareMixin):

    ALLOWED_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')

    def process_request(self, request):
        if request.method in self.ALLOWED_METHODS and request.content_type == "application/json":
            try:
                setattr(request, request.method, json.loads(request.body.decode('utf8')))
            except ValueError as ve:
                return HttpResponseBadRequest("Unable to parse JSON data. Error : {}".format(ve))
