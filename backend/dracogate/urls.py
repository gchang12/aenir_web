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
    #path("morphs/<int:pk>/<str:method>/", views.MorphMethodView.as_view(), name="morph_method"),
    path("morphs/<int:pk>/level_up/", views.LevelUpView.as_view(), name="level_up"),
    #path("morphs/<int:pk>/promote/", views.PromoteView.as_view(), name="promote"),
    #path("morphs/<int:pk>/use_stat_booster/", views.UseStatBoosterView.as_view(), name="use_stat_booster"),
    #path("morphs/<int:pk>/set_scrolls/", views.SetScrollsView.as_view(), name="set_scrolls"),
    #path("morphs/<int:pk>/use_afas_drops/", views.UseAfasDropsView.as_view(), name="use_afas_drops"),
    #path("morphs/<int:pk>/use_metiss_tome/", views.UseMetissTomeView.as_view(), name="use_metiss_tome"),
    #path("morphs/<int:pk>/set_bands/", views.SetBandsView.as_view(), name="set_bands"),
    #path("morphs/<int:pk>/shapeshift/", views.ShapeshiftView.as_view(), name="shapeshift"),
    #path("modify_morphs/level_up/<int:pk>/", views.LevelUpView.as_view(), name="level_up"),
    #path("morphs/<str:morph_id>/", views.ModifyMorphView.as_view(), name="modify_morph"),
    path("_preview/stats/<int:pk>/", views.ModifyMorphPreviewView.as_view(), name="modify_morph_preview"),
    path("_preview/create_morph/FE<int:game_no>/<str:name>/", views.UnitConfirmPreviewView.as_view(), name="unit_confirm_preview"),
]
