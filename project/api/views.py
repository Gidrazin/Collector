from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from api.serializers import (UserSerializer, ChangePasswordSerializer,
                              CollectSerializer, PaymentSerializer
                            )
from users.models import User
from main.models import Collect, Payment

def del_token_view():
    pass

def get_token_view():
    pass


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    pagination_class = PageLimitPagination
#    permission_classes = AllowAny,

#    @action(
#        detail=False,
#        methods=['get'],
#        permission_classes=(IsAuthenticated,)
#    )
#    def me(self, request):
#        user = User.objects.get(username=request.user)
#        serializer = self.get_serializer(user, many=False)
#        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
#        permission_classes=(IsAuthenticated,)
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
    serializer_class = CollectSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
