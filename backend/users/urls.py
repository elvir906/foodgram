from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('1/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
