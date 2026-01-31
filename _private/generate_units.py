"""
"""

import json

from aenir.morph import (
    Morph4,
    Morph5,
    Morph6,
    Morph7,
    Morph8,
    Morph9,
)

MORPHS = {
    4: Morph4,
    5: Morph5,
    6: Morph6,
    7: Morph7,
    8: Morph8,
    9: Morph9,
}

KWARGS_SET = {
    4: {"father": "Arden"},
    5: {},
    6: {"hard_mode": False, "number_of_declines": 0, "route": "Lalum"},
    7: {"lyn_mode": False, "hard_mode": False},
    8: {},
    9: {},
}

UNITS = []

for i in range(4, 9):
    morph_cls = MORPHS[i]
    kwargs = KWARGS_SET[i]
    for name in morph_cls.get_true_character_list():
        morph = morph_cls(name, **kwargs)
        unit = {
            "game": i,
            "name": name,
            "class": morph.current_cls,
            "lv": morph.current_lv,
        }
        UNITS.append(unit)

with open("UNITS.json", mode="w") as wfile:
    json.dump(UNITS, wfile, indent=2)
