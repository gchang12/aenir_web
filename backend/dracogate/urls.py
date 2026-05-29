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
    path("_preview/morph/FE<int:game_no>/<str:name>/", views.PreviewMorphView.as_view(), name="_preview_morph"),
    path("_preview/stats/<int:pk>/", views.PreviewStatsView.as_view(), name="_preview_stats"),
    path("modify_morphs/", views.ListMorphsView.as_view(), name="list_morphs"),
    path("modify_morphs/<int:pk>/", views.ModifyMorphView.as_view(), name="modify_morph"),
    #path("modify_morphs/level_up/<int:pk>/", views.LevelUpView.as_view(), name="level_up"),
    #path("modify_morphs/<str:morph_id>/", views.ModifyMorphView.as_view(), name="modify_morph"),
]
