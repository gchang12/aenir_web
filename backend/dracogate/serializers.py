"""
"""

from rest_framework import serializers

class InitArgs(serializers.Serializer):
    """
    """
    game_no = serializers.IntegerField(
        min_value=4,
        max_value=9,
    )
    name = serializers.CharField(
        min_length=1,
        max_length=9,
    )
    father = serializers.CharField(
        allow_null=True,
        default=None,
        min_length=1,
        max_length=9,
    )
    route = serializers.CharField(
        allow_null=True,
        default=None,
        min_length=5,
        max_length=6,
    )
    number_of_declines = serializers.IntegerField(
        allow_null=True,
        default=None,
        min_value=0,
        max_value=3,
    )
    lyn_mode = serializers.BooleanField(
        allow_null=True,
        default=None,
    )
    hard_mode = serializers.BooleanField(
        allow_null=True,
        default=None,
    )

class LevelUpArgs(serializers.Serializer):
    """
    """
    num_levels = serializers.IntegerField(
        min_value=1,
    )

class PromoteArgs(serializers.Serializer):
    """
    """
    promo_cls = serializers.CharField(
        min_value=1,
        allow_null=True,
    )

class UseStatBoosterArgs(serializers.Serializer):
    """
    """
    item_name = serializers.CharField(
        min_value=1,
    )

class ScrollEquipmentArgs(serializers.Serializer):
    """
    """
    scroll_name = serializers.CharField(
        min_value=1,
    )

class BandEquipmentArgs(serializers.Serializer):
    """
    """
    band_name = serializers.CharField(
        min_value=1,
    )

'''
# init
game_no
name
## Options
father
number_of_declines
lyn_mode
hard_mode
route
# level_up
num_levels
# promote
promo_cls
# use_stat_booster
item_name
# equip_scroll
scroll_name
# unequip_scroll
scroll_name
# use_afas_drops
# use_metiss_tome
# equip_knight_ward
# equip_band
band_name
# unequip_band
band_name
'''

class MorphSerializer:#(serializers.Serializer):
    """
    """
    #unitClass = serializers.CharField()
    #level = serializers.JSONField()
    #stats = StatsSerializer()

    def __init__(self, morph):
        """
        """
        self.morph = morph
        #self.stats = StatsSerializer(morph)

    def get_morph(self, *statdicts):
        """
        Bundles a morph's attributes for display purposes.
        """
        morph = self.morph
        stats = list(map(lambda stat: (stat, *map(lambda statdict: statdict[stat], statdicts)), morph.Stats.STAT_LIST()))
        return {
            "unitClass": morph.current_cls,
            "level": (morph.current_lv, morph.max_level),
            "stats": stats,
        }

    def get_current_stats(self):
        """
        Bundles stats for default display-purposes.
        """
        morph = self.morph
        current_stats = morph.current_stats.as_dict()
        max_stats = morph.max_stats.as_dict()
        absmax_stats = dict(zip(morph.Stats.STAT_LIST(), morph.Stats.ABSOLUTE_MAXES()))
        statdicts = (current_stats, max_stats, absmax_stats)
        return list(map(lambda dictlike: self.divide_by_100(dictlike), statdicts))

    def get_growth_rates(self):
        """
        Bundles growth augments for FE5, FE7, FE8, and FE9.
        """
        morph = self.morph
        old_growths = morph._og_growth_rates.as_dict()
        new_growths = morph.growth_rates.as_dict()
        growths_diff = morph.get_growth_augment().as_dict()
        statdicts = (old_growths, new_growths, growths_diff)
        return list(map(lambda dictlike: self.divide_by_100(dictlike), statdicts))

    def get_level_up_bonuses(self, num_levels: int):
        """
        Bundles level-up stats for FE5, FE7, FE8, and FE9.
        """
        morph = self.morph
        bonus_without_augment = (morph._og_growth_rates * num_levels).as_dict()
        augment = (morph.get_growth_augment() * -num_levels).as_dict()
        for stat in morph.Stats.ZERO_GROWTH_STAT_LIST():
            bonus_without_augment[stat] = None
            augment[stat] = None
        statdicts = (bonus_without_augment, augment)
        return list(map(lambda dictlike: self.divide_by_100(dictlike), statdicts))

    def get_stat_differences(self, morph2):
        """
        Bundles stat differences between Morphs into native Python data-type.
        """
        morph1 = self.morph
        morph_diff = (morph1.current_stats > morph2.current_stats).as_dict()
        statdicts = (morph_diff,)
        return list(map(lambda dictlike: self.divide_by_100(dictlike), statdicts))

    @staticmethod
    def divide_by_100(dictlike):
        """
        """
        new_dictlike = {}
        for stat, value in dictlike.items():
            if value is None:
                new_value = None
            else:
                new_value = 0.01 * value
            new_dictlike[stat] = new_value
        return new_dictlike

    @staticmethod
    def parse_init_args(dictlike):
        """
        Parses default values from response and converts them for interpretation by program.
        """
        game_no = int(dictlike.get("game_no"))
        name = dictlike.get("name")
        morph_options = (
            "father",
            "hard_mode",
            "number_of_declines",
            "route",
            "lyn_mode",
        )
        kwargs = {key: dictlike.get(key) for key in morph_options if dictlike.get(key) is not None}
        for kwarg, kwval in kwargs.items():
            if kwarg in ("hard_mode", "lyn_mode"):
                kwargs[kwarg] = {
                    "true": True,
                    "false": False,
                }[kwval]
            if kwarg == "number_of_declines":
                kwargs[kwarg] = int(kwval)
        return (game_no, name, kwargs)

