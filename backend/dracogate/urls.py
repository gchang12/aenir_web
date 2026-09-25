"""
"""

from django.urls import path, include

from . import views

app_name = "dracogate"
urlpatterns = [
    path("create/", views.GameSelectView.as_view(), name="game_select"),
    path("create/FE<int:game_no>/", views.UnitSelectView.as_view(), name="unit_select"),
    path("create/FE<int:game_no>/<str:unit>/", views.UnitConfirmView.as_view(), name="unit_confirm"),
    path("components/create/FE<int:game_no>/<str:unit>/", views.UnitConfirmForecast.as_view(), name="unit_confirm_forecast"),
    path("", views.MorphListView.as_view(), name="morph_list"),
    path("<int:id>/", views.MorphDetailView.as_view(), name="morph_detail"),
    path("<int:id>/level_up/", views.LevelUpView.as_view(), name="level_up"),
    path("<int:id>/promote/", views.PromoteView.as_view(), name="promote"),
    path("<int:id>/use_stat_booster/", views.UseStatBoosterView.as_view(), name="use_stat_booster"),
    path("<int:id>/use_afas_drops/", views.UseAfasDropsView.as_view(), name="use_afas_drops"),
    path("<int:id>/use_metiss_tome/", views.UseMetissTomeView.as_view(), name="use_metiss_tome"),
    path("<int:id>/set_scrolls/", views.SetScrollsView.as_view(), name="set_scrolls"),
    path("<int:id>/set_bands/", views.LevelUpView.as_view(), name="set_bands"),
    path("<int:id>/shapeshift/", views.ShapeshiftView.as_view(), name="shapeshift"),
    path("<int:id>/set_demiband/", views.LevelUpView.as_view(), name="set_demiband"),
    path("components/<int:id>/action_forecast/", views.ActionForecastView.as_view(), name="action_forecast"),
    # TODO: component that allows user to rename the morph
]
