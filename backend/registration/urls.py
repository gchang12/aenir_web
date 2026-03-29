"""
"""

from django.urls import (
    path,
    include,
)

from registration import views

app_name = "registration"
urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
]#include("django.contrib.auth.urls")
