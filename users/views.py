import pdb

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, ChangePasswordSerializer, MeUpdateSerializer, MeSerializer


User = get_user_model()

@extend_schema_view(
    post=extend_schema(summary='Регистрация пользователя', tags=['Аутентификация & Авторизация']),
)
class RegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=ChangePasswordSerializer,
        summary='Смена пароля', tags=['Аутентификация & Авторизация']),
)
class ChangePasswordView(APIView):

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(
            instance=user, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary='Профиль пользователя', tags=['Пользователи']),
    # put=extend_schema(summary='Изменить профиль пользователя', tags=['Пользователи']),
    patch=extend_schema(summary='Изменить частично профиль пользователя', tags=['Пользователи']),
)
class MeView(RetrieveUpdateAPIView):
    '''Update List инфо о юзере на сайте, переопределяем метод для class_serialiser
    в зависимости от get patch put запроса и get_object что бы не вводить в url pk
    а пользователь будет браться из request.user'''
    queryset = User.objects.all()
    serializer_class = MeSerializer
    http_method_names = ('get', 'patch',) # скроем метод PUT в сваггере, определив конкретные методы

    def get_serializer_class(self):
        '''переопределяем class_serialiser для метода в зависимости от get patch put запроса'''
        if self.request.method in ('PUT', 'PATCH',):
            return MeUpdateSerializer
        return MeSerializer

    def get_object(self):
        '''что бы не вводить в url pk а пользователь будет браться из request.user'''
        return self.request.user


