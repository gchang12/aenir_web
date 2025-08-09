"""
"""

from django.urls import (
    path,
    include,
)
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'get_character_list', views.GetCharacterListView, 'get_character_list')

#app_name = "dracogate"
urlpatterns = [
    path('api/', include(router.urls)),
]
