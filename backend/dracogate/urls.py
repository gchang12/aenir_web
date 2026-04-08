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
    path("create_morph/FE<int:game_no>/", views.UnitSelectView.as_view(), name="unit_select"),
    path("create_morph/FE<int:game_no>/<str:name>/", views.UnitConfirmView.as_view(), name="unit_confirm"),
    path("_preview_morph/FE<int:game_no>/<str:name>/", views.PreviewMorphView.as_view(), name="_preview_morph"),
    path("modify_morphs/<uuid:id>/", views.ModifyMorphView.as_view(), name="modify_morph"),
]
