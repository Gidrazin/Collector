from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from api.serializers import (UserSerializer, ChangePasswordSerializer,
                              GetCollectSerializer, PostCollectSerializer, 
                              PaymentSerializer, GetTokenSerializer,
                            )
from api.permissions import IsAuthorOrReadOnly
from users.models import User
from main.models import Collect, Payment

@api_view(['POST'])
@permission_classes([AllowAny])
def get_token_view(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    user = get_object_or_404(User, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {'auth_token': str(token.key)},
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def del_token_view(request):
    Token.objects.get(user=request.user).delete()
    return Response(
        None,
        status=status.HTTP_204_NO_CONTENT,
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    pagination_class = PageLimitPagination
    permission_classes = AllowAny,

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = User.objects.get(username=request.user)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        user = User.objects.get(username=request.user)
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'status': 'password set'})


class CollectViewSet(viewsets.ModelViewSet):
    queryset = Collect.objects.all()
    permission_classes = IsAuthorOrReadOnly,

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetCollectSerializer
        return PostCollectSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        # Отправим e-mail
        send_mail(
            'Донат отправлен!',
            'Донат отправлен',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
        )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
