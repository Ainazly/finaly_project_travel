from django.urls import path, include

from .views import RegistrUserView, Verify_EmailAPIView, ChangePasswordView

urlpatterns = [
    path('register/', RegistrUserView.as_view()),
    path('verify/<uuid:ver_code>/', Verify_EmailAPIView.as_view()),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]


