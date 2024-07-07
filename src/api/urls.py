from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views.auth.registration_view import RegistrationView

urlpatterns = [
    path('registration', RegistrationView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
