"""
"""

from django.urls import path, include

from . import views

# TODO: https://docs.djangoproject.com/en/6.1/topics/auth/default/#module-django.contrib.auth.views
# TODO: All other authentication views. Ugh.
# TODO: view for creating account.

'''
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
'''

# logged-out/homepage: login/
# */login: register, password_reset
# logged-in/homepage: logout, password_change

urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
