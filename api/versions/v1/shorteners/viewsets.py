from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet

from api.models.shorteners.models import ShortURL
from api.versions.v1.shorteners.serializers import ShortenerCreateSerializer, ShortenerRedirectSerializer
from core.mixins import *


class ShortenerViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    MappingViewSetMixin,
    SimpleJWTMixin,
    GenericViewSet,
):
    serializer_action_map = {
        "create": ShortenerCreateSerializer,
        "redirect": ShortenerRedirectSerializer,
        "statistics": ShortenerCreateSerializer,
    }
    queryset = ShortURL.objects.filter(is_active=True)
    lookup_field = "short_url"

    def create(self, request, *args, **kwargs):
        """
        단축 url 생성

        **Description**
        - 단축 url 생성 API
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(tags=["v1"])
    def redirect(self, request, *args, **kwargs):
        """
        단축 url 이동

        **Description**
        - 단축 url redirect
        redirect 이기 때문에 api가 아닙니다.
        주소창에 바로 입력해주세요
        """
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer.perform_redirect()

    def statistics(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        res = {
            "origin_url": instance.origin_url,
            "request_count": instance.request_count,
            "daily_count": serializer.get_daily_count(instance),
            "weekly_count": serializer.get_weekly_count(instance),
        }
        return Response(res)
