"""
"""

from django.urls import path, include

from . import views

app_name = "dracogate"
urlpatterns = [
    path("create/", views.CreateMorphView.as_view(), name="morph_init"),
    path("create/FE<int:game_no>/", views.GameSelectView.as_view(), name="game_select"),
    path("create/FE<int:game_no>/<str:unit>/", views.UnitSelectView.as_view(), name="unit_select"),
    path("forms/create/FE<int:game_no>/<str:unit>/", views.UnitSelectForm.as_view(), name="unit_select_form"),
]
