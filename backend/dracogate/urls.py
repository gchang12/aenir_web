"""
"""

from django.contrib import admin
from django.urls import (
    path,
    include,
)

from . import views

app_name = "dracogate"
urlpatterns = [
    path("create_morph/", views.GameSelectView.as_view(), name="game_select"),
    path("create_morph/fe<int:game_no>/", views.UnitSelectView.as_view(), name="unit_select"),
]
