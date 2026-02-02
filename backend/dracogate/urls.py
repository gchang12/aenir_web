"""
"""

from django.urls import (
    include,
    path,
)
from rest_framework import routers

from dracogate import views

router = routers.DefaultRouter()
router.register(r"morphs", views.MorphViewSet, basename="morphs")

urlpatterns = [
    path("api/", include(router.urls)),
]
