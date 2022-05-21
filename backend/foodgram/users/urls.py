from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UsersCustomViewSet

app_name = 'users'


router_v1 = DefaultRouter()
router_v1.register('users', UsersCustomViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('users/auth/', include('djoser.urls.authtoken')),
]
