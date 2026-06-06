
from django.contrib import admin
from django.urls import path, include
from .router import router

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # Endpoint to log in and get access/refresh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Endpoint to get a new access token using a valid refresh token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
] 

urlpatterns += router.urls
