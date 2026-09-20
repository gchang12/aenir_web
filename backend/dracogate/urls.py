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
]
