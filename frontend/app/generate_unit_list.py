
import json
from aenir.morph import Morph4, Morph5, Morph6, Morph7, Morph8, Morph9
UNITS = {}
UNITS[4] = Morph4.get_true_character_list()
UNITS[5] = Morph5.get_true_character_list()
UNITS[6] = Morph6.get_true_character_list()
UNITS[7] = Morph7.get_true_character_list()
UNITS[8] = Morph8.get_true_character_list()
UNITS[9] = Morph9.get_true_character_list()
for k, v in UNITS.items():
    UNITS[k] = list(v)
with open("UNITS.ts", mode="w") as wfile:
    json.dump(UNITS, wfile, indent=2)
