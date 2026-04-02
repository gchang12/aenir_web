"""
"""

from django.urls import (
    path,
    include,
)

from .views import CreateAccountView

app_name = "accounts"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("create_account/", CreateAccountView.as_view(), name="create_account"),
]
