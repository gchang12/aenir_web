"""
"""

from django.urls import (
    path,
    include,
)

from rest_framework.authtoken import views as token_views 

from .views import CreateAccountView

app_name = "registration"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("create-account/", CreateAccountView.as_view(), name="create-account"),
    path("obtain-auth-token/", token_views.obtain_auth_token, name="obtain-auth-token"),
]
