from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


urlpatterns = [
    path("", views.ListRegisterUserView.as_view(), name="users"),
    path("<int:pk>/", views.RetrieveUpdateDestroyUserView.as_view(), name="user"),
    path("<int:pk>/send_verification/", views.SendVerificationView.as_view(), name="send_verification"),
    path("<int:pk>/verification/", views.VerificationView.as_view(), name="verification"),
    path("<int:pk>/delete_account/", views.DeleteAccountView.as_view(), name="delete_account"),
    path("<int:pk>/change_active_status/", views.ChangeActiveStatusView.as_view(), name="change_active"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("me/", views.MeView.as_view(), name="me"),
    path('token/', TokenObtainPairView.as_view(), name = 'token'),
    path('refresh/token/', TokenRefreshView.as_view(), name = 'token_refresh'),
]
