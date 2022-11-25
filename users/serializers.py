# Подключаем класс для работы со сериалайзер
from rest_framework import serializers
# Подключаем модель user
from .models import CustomUser


# Создаём класс UserRegistrSerializer
class UserRegistrSerializer(serializers.ModelSerializer):
    # Поле для повторения пароля
    password2 = serializers.CharField()
    token = serializers.CharField(
        max_length=256,
        read_only=True
    )

    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = CustomUser
        # Назначаем поля которые будем использовать
        fields = ['email', 'username', 'phone_number', 'password', 'password2', 'token']

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = CustomUser(
            email=self.validated_data['email'],  # Назначаем Email
            username=self.validated_data['username'],  # Назначаем Логин
            # phone_number=self.validated_data['phone_number']
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user


class VerifySerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('ver_code', 'email',)


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)



