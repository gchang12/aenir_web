"""
"""

from django.shortcuts import render

from rest_framework import viewsets

from . import serializers

class GetCharacterListView(viewsets.):
    """
    """
    serializer_class = serializers.
