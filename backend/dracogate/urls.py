"""
URLs for views, to be inserted or loaded.
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
    # TODO: Think of better names for these.
    path("morphs/", views.ListMorphsView.as_view(), name="list_morphs"),
    path("morphs/<int:pk>/", views.ModifyMorphView.as_view(), name="modify_morph"),
    #path("modify_morphs/level_up/<int:pk>/", views.LevelUpView.as_view(), name="level_up"),
    #path("morphs/<str:morph_id>/", views.ModifyMorphView.as_view(), name="modify_morph"),
    path("_preview/create_morph/FE<int:game_no>/<str:name>/", views.UnitConfirmPreviewView.as_view(), name="unit_confirm_preview"),
    path("_preview/stats/<int:pk>/", views.ModifyMorphPreviewView.as_view(), name="modify_morph_preview"),
]
