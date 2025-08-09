"""
"""

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response

from aenir.morph import (
    Morph4,
    Morph5,
    Morph6,
    Morph7,
    Morph8,
    Morph9,
)

class InitializationViewset(viewsets.ViewSet):
    """
    """

    def list(self, request):
        """
        """
        game = request.GET.get("game")
        morph_class = {
            4: Morph4,
            5: Morph5,
            6: Morph6,
            7: Morph7,
            8: Morph8,
            9: Morph9,
        }[int(game)]
        character_list = list(morph_class.get_true_character_list())
        return Response(character_list)

    def create(self, request):
        """
        """

    def update(self, request):
        """
        """

