"""
"""

from django.urls import (
    path,
    include,
)
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'initialize_morph', views.InitializationViewset, basename='initialize_morph')
router.register(r'preview_morph', views.PreviewViewset, basename='preview_morph')

app_name = "dracogate"
urlpatterns = [
    path('api/', include(router.urls)),
]

