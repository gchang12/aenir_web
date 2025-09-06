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

from ._logging import logger

def convert_js_boolean_to_python_boolean(value):
    """
    """
    try:
        return {
            'true': True,
            'false': False,
            'on': True,
            'off': False,
        }[value]
    except KeyError:
        return value

def convert_str_to_int(value):
    """
    """
    if not isinstance(value, str):
        return value
    try:
        return int(value)
    except ValueError:
        return value

class InitializationViewset(viewsets.ViewSet):
    """
    """

    def list(self, request):
        """
        """
        data = {}
        for key, value in request.query_params.items():
            value = convert_str_to_int(value)
            value = convert_js_boolean_to_python_boolean(value)
            data[key] = value
        data['game_no'] = int(data.pop("game"))
        name = data.get("name")
        game = data.get('game_no')
        logger.debug("Getting character: %s from FE%d", name, game)
        try:
            morph = get_morph(**data)
            logger.debug("Got Morph%d instance of %s", game, name)
            return Response([
                True, {
                    "current_stats": morph.current_stats.as_list(),
                    "current_maxes": morph.max_stats.as_list(),
                    "current_cls": morph.current_cls,
                    "current_lv": morph.current_lv,
                }
            ])
        except InitError as err:
            logger.debug("Failed to fetch Morph%d!%s. Need extra data: %s, %s", game, name, err.init_params, err.init_params2)
            # implicit: bind first item of err-initparams to `missing_params`
            for missing_params in err.init_params.items():
                break
            # implicit: bind first item of err-initparams2 to `missing_params2` if applicable
            if err.init_params2 is None:
                missing_params2 = None
            else:
                for missing_params2 in err.init_params2.items():
                    break
            return Response([
                False, {
                    "missing_params": missing_params,
                    "missing_params2": missing_params2,
                }
            ])

    def create(self, request):
        """
        """
        # TODO: Use this for, like, saving the morph.
        # save to session or whatever
        init_kwargs = request.data['data']
        init_kwargs['game_no'] = int(init_kwargs.pop('game'))
        for key, value in init_kwargs.items():
            value = convert_js_boolean_to_python_boolean(value)
            value = convert_str_to_int(value)
            init_kwargs[key] = value
        print(init_kwargs)
        try:
            morph = get_morph(**init_kwargs)
        except InitError as err:
            # implicit: bind first item of err-initparams to `missing_params`
            for missing_params in err.init_params.items():
                break
            key1, val1 = missing_params
            init_kwargs[key1] = val1[0]
            # implicit: bind first item of err-initparams2 to `missing_params2` if applicable
            if err.init_params2 is None:
                missing_params2 = None
            else:
                for missing_params2 in err.init_params2.items():
                    break
                key2, val2 = missing_params2
                init_kwargs[key2] = val2[0]
            morph = get_morph(**init_kwargs)
        request.session.setdefault("morphs", [])
        json_morph = {
            "class": morph.__class__.__name__,
            "morph": {
                "game": morph.game,
                "name": morph.name,
                "current_cls": morph.current_cls,
                "current_lv": morph.current_lv,
                "current_stats": morph.current_stats.as_list(),
                "current_maxes": morph.max_stats.as_list(),
                "history": morph.history,
                "_meta": morph._meta,
            },
            "actions": [
                ("__init__", init_kwargs),
            ],
        }
        morphs = request.session.get("morphs")
        morphs.append(json_morph)
        #request.session.modified = True
        request.session.save()
        print("InitializationViewset:", morphs)
        return Response(morphs)

class PreviewViewset(viewsets.ViewSet):
    """
    """

    def list(self, request):
        """
        """
        request.session.setdefault('morphs', [])
        morphs = request.session.get('morphs')
        print(morphs)
        return Response([morph['morph'] for morph in morphs])

    def create(self, request):
        """
        """
        data = request.data['data']
        print("PreviewViewset.data:", data)
        request.session.setdefault('morphs', [])
        morphs = request.session.get('morphs')
        morphs.extend([record['morph'] for record in data])
        #request.session.modified = True
        request.session.save()
        print("PreviewViewset.morphs:", morphs)
        return Response()

