"""
"""

from django.shortcuts import render
from django.views.generic import base

class HomePageView(base.TemplateView):
    """
    """
    template_name = "_base.html"
