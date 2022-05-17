from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UsersCustomViewSet

app_name = 'users'

router = DefaultRouter()
router.register('users', UsersCustomViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
