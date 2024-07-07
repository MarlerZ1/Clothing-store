from django.contrib.auth.views import LogoutView
from django.urls import path
from users.views import UserLoginView, UserRegistrationView, UserProfileView, UserLogoutView

app_name = 'users'

urlpatterns = [
    path('login', UserLoginView.as_view(), name="login"),
    path('registration', UserRegistrationView.as_view(), name="registration"),
    path("profile", UserProfileView.as_view(), name="profile"),
    path("logout", UserLogoutView.as_view(), name="logout")
]