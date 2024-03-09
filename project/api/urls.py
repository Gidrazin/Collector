from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (del_token_view, get_token_view, UserViewSet,
                       CollectViewSet, PaymentViewSet)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('collects', CollectViewSet)
router.register('payments', PaymentViewSet)


token_urls = [
    path('login/', get_token_view, name='login'),
    path('logout/', del_token_view, name='logout'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', include(token_urls)),
]
