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
from aenir._exceptions import InitError

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
        print(character_list)
        return Response(character_list, content_type="text/json")

    def create(self, request):
        """
        """
        print("data", request.data)
        data = request.data.pop('data')
        data['game_no'] = int(data.pop("game"))
        #name = data.get("name")
        #print(data)
        try:
            morph = get_morph(**data)
            print("success")
            print(morph.current_stats.as_list())
            print([morph.current_cls, morph.current_lv])
            return Response([True, (morph.current_cls, morph.current_lv), morph.current_stats.as_list()])
        except InitError as err:
            print("request failed")
            #print(list(err.init_params.items()))
            #for missing_params in err.init_params: pass
            #missing_params = list(dict(err.init_params).items())
            missing_params = err.init_params.popitem()
            print("missing_params: " + str(missing_params))
            return Response([False, None, missing_params])

    def update(self, request):
        """
        """
        data = request.data.pop('data')
        morph_id = data.pop('morphId')
        self.session.set("morphs", {})
        morphs = self.session.get("morphs")
        if morph_id in morphs:
            return Response([False, ("morph_id", morph_id)])
        data['game_no'] = int(data.pop("game"))
        morphs[morph_id] = [("__init__", data)]
        self.session.save()
        return Response([True, morphs[morph_id]])
        # REDIRECT TO HOME AFTERWARDS
