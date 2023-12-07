from django.core import serializers
from django.db.models import Model
from django.http import JsonResponse, HttpRequest

from dennis_systems.core.shared_lib.auth.Authorization import Authorization
from dennis_systems.core.shared_lib.service.DefaultService import DefaultService


def to_result(item: Model):
    from django.forms.models import model_to_dict
    return JsonResponse(model_to_dict(item))
    # return JsonResponse(serializers.serialize("json", [item.__class__.objects.last()]), safe=False)


class ApiDefault:
    __service: DefaultService

    def __init__(self, service : DefaultService):
        self.__service = service

    def list(self, request: HttpRequest, limit: int, page: int) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.list(limit, page))
        pass

    def save(self, item: Model, request: HttpRequest) -> JsonResponse:
        self.check_token(request)
        return to_result(self.get_service().save(item))

    def delete(self, request: HttpRequest, item: Model) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.delete(item))

    def get(self, request: HttpRequest, id: int) -> JsonResponse:
        self.check_token(request)
        return JsonResponse(self.__service.get(id), safe=False)

    def get_service(self):
        return self.__service

    @staticmethod
    def to_model(model: Model):
        return JsonResponse(model.__dict__)

    @staticmethod
    def check_token(request: HttpRequest) -> None:
        if not Authorization.has_auth_token(request):
            print('not token')
        else:
            print('token_found')
            Authorization.parce_token(request)
