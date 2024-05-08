from django.contrib.auth.hashers import check_password

from core.tokens import TokenResponseSerializer
from users.models import User
from rest_framework.request import Request
from rest_framework.views import APIView

from core.constants import SystemCodeManager
from core.exceptions import raise_exception
from core.responses import Response

from .serializers.register_serializers import RegisterSerializer
from .serializers.login_serializers import LoginSerializer


class RegisterView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            raise_exception(
                code=SystemCodeManager.get_message("base_code", "INVALID_FORMAT")
            )

        serializer.save()
        return Response(data=serializer.data)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request: Request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)

            if check_password(password, user.password):
                serializer = TokenResponseSerializer(user)
                return Response(data=serializer.to_representation(serializer))
            else:
                raise raise_exception(
                    code=SystemCodeManager.get_message("auth_code", "USER_INVALID_PW")
                )
        except User.DoesNotExist:
            raise raise_exception(
                code=SystemCodeManager.get_message("auth_code", "USER_NOT_FOUND")
            )
