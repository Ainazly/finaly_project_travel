from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from phonenumber_field.modelfields import PhoneNumberField
from uuid import uuid4
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework.reverse import reverse


# Создаем класс менеджера пользователей
class MyUserManager(BaseUserManager):
    use_in_migrations = True

    # Создаём метод для создания пользователя
    def _create_user(self, email=None, username=None
                     , password=None, phone_number=None, **extra_fields):
        if not username:
            if not email and not phone_number:
                raise ValueError('The given email/phone must be set')

        if email:
            email = self.normalize_email(email)

            if not username:
                username = email

            user = self.model(
                email=email,
                username=username,
                **extra_fields
            )

        if phone_number:
            if not username:
                username = phone_number

            user = self.model(
                username=username,
                phone=phone_number,
                **extra_fields
            )

            # проверяем является ли пользователь
            # суперпользователем
        if extra_fields.get('is_superuser'):
            user = self.model(
                username=username,
                **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            username=username,
            password=password,
            **extra_fields
        )


class CustomUser(AbstractUser):
    name_surname = models.CharField('ФИО', max_length=100, blank=False, null=True)
    birth_date = models.DateField('Дата рождения', blank=False, null=True, default='2000-01-12')
    phone_number = PhoneNumberField(null=True, region='KG', unique=True)  # номер телефона
    email = models.EmailField(max_length=100, unique=True)  # Почта
    ver_code = models.UUIDField(default=uuid4)
    is_active = models.BooleanField(default=False)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа

    USERNAME_FIELD = 'username'  # Идентификатор для обращения
    REQUIRED_FIELDS = ['email']  # хранит список имён при регистрации  для Superuser

    objects = MyUserManager()  # Добавляем методы класса MyUserManager

    def __str__(self):
        return self.email

    def generate_uuid(self):
        self.ver_code = uuid4()
        self.save(update_fields=['ver_code'])


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    email_confirmed = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, default='2000-09-12')
    phone_number = PhoneNumberField(null=True, region='KG', unique=True)

    # confirmation_token = default_token_generator.make_token(CustomUser.user)
    # actiavation_link = f'{activate_link_url}user_id={user.id}&confirmation_token={confirmation_token}'


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        host = 'http://127.0.0.1:8000/verify/'
        token = default_token_generator.make_token(user=instance)
        # user = instance.id
        send_mail('tours@gmail.com',
                  f'''
            Здравствуйте , {instance.username} \n
            Для завершения регистрации, перейдите по ссылке,
            http://127.0.0.1:8000/verify/{instance.ver_code}''',
                  settings.EMAIL_HOST_USER,
                  [instance.email],
                  fail_silently=False,
                  )
        UserProfile.objects.create(user=instance)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # new_uuid = instance.generate_uuid()
    email_plaintext_message = reset_password_token.key

    send_mail(
        "Восстановление пароля",
        f'''
        Ваш токен для восстановления пароля
        Токен: {email_plaintext_message} . 
        Перейдите по ссылке, введите ваш токен и новый пароль
        http://127.0.0.1:8000/api/password_reset/confirm/ ''',
        "tours@gmail.com",
        [reset_password_token.user.email]
    )
