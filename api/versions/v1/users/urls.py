from rest_framework.routers import SimpleRouter
from rest_framework.urls import path

from .viewsets import UserViewSet

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path("users", UserViewSet.as_view({"post": "create"})),
    path("users/<int:pk>", UserViewSet.as_view({"get": "retrieve", "delete": "destroy", "patch": "partial_update"})),
    path("users/login", UserViewSet.as_view({"post": "login"})),
    path("users/logout", UserViewSet.as_view({"get": "logout"})),
]
