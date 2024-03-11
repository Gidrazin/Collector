from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from django.db.models import Sum
from drf_base64.fields import Base64ImageField
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


class PaymentSerializer(ModelSerializer):
    user = UserSerializer(
        read_only=True
    )

    class Meta:
        model = Payment
        fields = ('user', 'event', 'amount')


class GetCollectSerializer(ModelSerializer):
    author = UserSerializer(
        read_only=True
    )
    payments = PaymentSerializer(
        many=True
    )
    payments_cnt = SerializerMethodField()
    current = SerializerMethodField()

    def get_payments_cnt(self, obj):
        return obj.payments.count()

    def get_current(self, obj):
        return obj.payments.aggregate(Sum('amount'))['amount__sum']

    class Meta:
        model = Collect
        fields = (
            'author',
            'payments',
            'payments_cnt',
            'title',
            'reason',
            'image',
            'description',
            'total',
            'current',
            'start',
            'end'
        )

class PostCollectSerializer(ModelSerializer):
    image = Base64ImageField(
        required=False,
        allow_null=True,
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Collect
        fields = (
            'author',
            'payments',
            'title',
            'reason',
            'image',
            'description',
            'total',
            'start',
            'end'
        )

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
