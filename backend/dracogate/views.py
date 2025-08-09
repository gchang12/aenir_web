"""
"""

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response

from aenir import get_morph
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
        data = request.data['data']
        game = int(data.get("game"))
        name = data.get("name")
        print(data)
        try:
            morph = get_morph(game, name)
            print(morph.current_stats.as_list())
            return Response(morph.current_stats.as_list())
        except:
            print("request failed")
            return Response([])

    def update(self, request):
        """
        """

