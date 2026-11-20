from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.OtpRequestView.as_view(), name="request_otp"),
    path("verify/", views.OtpVerifyView.as_view(), name="verify_otp"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileUpdateView.as_view(), name="profile"),
]
