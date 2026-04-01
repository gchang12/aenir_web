"""
"""

from django.urls import (
    path,
    include,
)
from django.views.generic.base import RedirectView

from rest_framework.authtoken import views as token_views 

from .views import CreateAccountView

app_name = "accounts"
urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    #registration/login/ [name='login']
    #registration/logout/ [name='logout']
    #registration/password_change/ [name='password_change']
    #registration/password_change/done/ [name='password_change_done']
    #registration/password_reset/ [name='password_reset']
    #registration/password_reset/done/ [name='password_reset_done']
    #registration/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    #registration/reset/done/ [name='password_reset_complete']
    path("create-account/", CreateAccountView.as_view(), name="create-account"),
    path("obtain-auth-token/", token_views.obtain_auth_token, name="obtain-auth-token"),
    path("profile/", RedirectView.as_view(url="http://localhost:3000/"), name="profile"),
]
