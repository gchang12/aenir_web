"""
"""

from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
