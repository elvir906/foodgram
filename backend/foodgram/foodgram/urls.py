from django.contrib import admin
from django.urls import path
# from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('recipes.urls', namespace='recipes')),
    # path('auth/', include('users.urls', namespace='users')),
    # path('auth/', include('django.contrib.auth.urls')),
]
