from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from api.views.auth.logout_view import LogoutView
from api.views.auth.registration_view import RegistrationView
from api.views.user.get_all_users_view import GetUsersView
from api.views.user.get_or_patch_user_by_id_view import GetOrPatchUserView

user_urlpatterns = [
    path('list', GetUsersView.as_view()),
    path('<int:id>', GetOrPatchUserView.as_view())
]

urlpatterns = [
    path('registration', RegistrationView.as_view()),
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout', LogoutView.as_view()),
    path('token-refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', include(user_urlpatterns))
]
