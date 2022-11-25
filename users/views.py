# Подключаем статус
from django.contrib.auth.tokens import default_token_generator
from django.db.migrations import serializer
from rest_framework import status
from rest_framework.decorators import action
# Подключаем компонент для ответа
from rest_framework.response import Response
# Подключаем компонент для создания данных
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
# Подключаем компонент для прав доступа
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

# Подключаем модель User
from .models import CustomUser
# Подключаем UserRegistrSerializer
from .serializers import UserRegistrSerializer, VerifySerializer, ChangePasswordSerializer


# Создаём класс RegistrUserView
class RegistrUserView(CreateAPIView):
    # Добавляем в queryset
    queryset = CustomUser.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    @action(detail=False, permission_classes=[AllowAny], methods=['get'])
    def activate(self, request, pk=None):
        user_id = request.query_params.get('user_id', '')
        token = request.query_params.get('confirmation_token', '')
        try:
            user = self.get_queryset().get(pk=user_id)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is None:
            return Response('User not found', status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response('Token is invalid or expired. Please request another confirmation email by signing in.',
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return Response('Email successfully confirmed')

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)


class Verify_EmailAPIView(RetrieveAPIView):
    serializer_class = VerifySerializer
    queryset = CustomUser.objects.filter(is_active=False)

    lookup_field = "ver_code"

    def retrieve(self, request, *args, **kwargs):
        instance: CustomUser = self.get_object()
        serializer = self.get_serializer(instance)
        instance.is_active = True
        instance.save()
        return Response(serializer.data)


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Пароль неверный"]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





