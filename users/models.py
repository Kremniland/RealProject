from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ParseError

from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        if not (email or phone_number or username):
            raise ParseError('Укажите email или телефон')

        if email:
            email = self.normalize_email(email)

        if not username:
            if email:
                username = email.split('@')[0]
            else:
                username = phone_number

        user = self.model(username=username, **extra_fields)
        if email:
            user.email = email
        if phone_number:
            user.phone_number = phone_number

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )

    def create_superuser(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )


class User(AbstractUser):
    username = models.CharField(
        'Никнейм', max_length=64, unique=True, null=True, blank=True
    )
    email = models.EmailField('Почта', unique=True, null=True, blank=True)
    phone_number = PhoneNumberField('Телефон', unique=True, null=True, blank=True)
    USERNAME_FIELD = 'username' # Поле используется в качастве имени
    REQUIRED_FIELDS = ['phone_number'] # Запрашивается при создании суперюзера

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'


class Profile(models.Model):
    user = models.OneToOneField(
        'users.User', models.CASCADE, related_name='profile',
        verbose_name='Пользователь', primary_key=True,
    )
    telegram_id = models.CharField(
        'Telegram ID', max_length=20, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user} ({self.pk})'


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    '''Используя сигнал создаем профиль при создании пользователя'''
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
