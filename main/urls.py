from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('tour/', include('tours.urls')),
    # path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
