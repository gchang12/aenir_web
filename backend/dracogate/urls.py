"""
"""

from django.urls import (
    path,
    include,
)

from . import views

app_name = "dracogate"
urlpatterns = [
    path("get_character_list", views., name="get_character_list"),
]
