"""
"""

from django.urls import path, include

from . import views

app_name = "dracogate"
urlpatterns = [
    path("create/", views.GameSelectView.as_view(), name="game_select"),
    path("create/FE<int:game_no>/", views.UnitSelectView.as_view(), name="unit_select"),
    path("create/FE<int:game_no>/<str:unit>/", views.UnitConfirmView.as_view(), name="unit_confirm"),
    path("forms/create/FE<int:game_no>/<str:unit>/", views.UnitConfirmForm.as_view(), name="unit_confirm_form"),
]
