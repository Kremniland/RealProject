from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ParseError

from .models import Profile

User = get_user_model()


class ProfileShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'telegram_id',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    # переопределяем поле password  write_only=True чтобы поле
    # с паролем не возвращалось при ответе, что бы не было его видно
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password',)

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'Пользователь с такой почтой уже зарегистрирован.'
            )
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        '''захэширует пароль в базе'''
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')

    def validate(self, attrs):
        user = self.instance
        old_password = attrs.pop('old_password')
        if not user.check_password(old_password):
            raise ParseError(
                'Проверьте правильность текущего пароля.'
            )
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('new_password')
        instance.set_password(password)
        instance.save()
        return instance


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileShortSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
            'date_joined',
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileShortSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'username',
            'profile',
        )

    # def update(self, instance, validated_data):
    # '''Можно так но лучше вынести логику в сериалайзер ProfileUpdateSerializer'''
    #     # Проверка наличия профиля
    #     profile_data = validated_data.pop('profile') if 'profile' in validated_data else None
    #     instance = super().update(instance, validated_data)
    #
    #     if profile_data:
    #         profile = instance.profile
    #         for key, value in profile_data.items(): # проходим по данным и забираем ключ значение
    #             if hasattr(profile, key): # Проверяем есть ли в профиле такой ключ
    #                 setattr(profile, key, value) # если ключ есть то заносим туда value
    #         profile.save()
    #     return instance

    def update(self, instance, validated_data):
        '''Выносим основную логику в ProfileUpdateSerializer при изменении полей в профиле'''
        # Проверка наличия профиля
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None

        with transaction.atomic():
            instance = super().update(instance, validated_data)

            # Update профиля
            self._update_profile(instance.profile, profile_data)

        return instance

    def _update_profile(self, profile, data):
        profile_serializer = ProfileUpdateSerializer(
            instance=profile, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
