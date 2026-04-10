"""
"""

from django.urls import (
    path,
    include,
)

from . import views

app_name = "accounts"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("create_account/", views.CreateAccountView.as_view(), name="create_account"),
]
