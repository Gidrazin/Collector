from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from rest_framework.serializers import (CharField, EmailField, ImageField,
                                        IntegerField, ModelSerializer,
                                        ReadOnlyField, Serializer,
                                        SerializerMethodField,
                                        SlugRelatedField, ValidationError)

from main.models import Collect, Payment
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'id',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_field = ('id', )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('Этот email уже занят!')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(Serializer):
    new_password = CharField(required=True)
    current_password = CharField(required=True)

    def validate(self, data):
        password = data.get('current_password')
        user = self.context['request'].user
        if not user.check_password(password):
            raise ValidationError(
                'Текущий пароль неверный!'
            )
        return data


class CollectSerializer(ModelSerializer):
    class Meta:
        model = Collect
        fields = '__all__'


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class GetTokenSerializer(Serializer):
    password = CharField(required=True)
    email = EmailField(required=True)

    def validate(self, data):
        user = authenticate(
            username=data.get('email'),
            password=data.get('password')
        )
        if user is None:
            raise ValidationError(
                'Пара password, email в базе не найдена!'
            )
        return data
