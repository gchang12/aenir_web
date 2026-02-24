"""
"""

from rest_framework import serializers

class MorphSerializer(serializers.Serializer):
    """
    """

    @staticmethod
    def serialize_morph(morph, *statdicts):
        """
        Bundles a morph's attributes for display purposes.
        """
        stats = list(map(lambda stat: (stat, *map(lambda statdict: statdict[stat], statdicts)), morph.Stats.STAT_LIST()))
        return {
            "unitClass": morph.current_cls,
            "level": (morph.current_lv, morph.max_level),
            "stats": stats,
        }

    @staticmethod
    def serialize_current_stats(morph):
        """
        Bundles stats for default display-purposes.
        """
        current_stats = (morph.current_stats * 0.01).as_dict()
        max_stats = (morph.max_stats * 0.01).as_dict()
        absmax_stats = dict(zip(morph.Stats.STAT_LIST(), morph.Stats.ABSOLUTE_MAXES()))
        statdicts = [current_stats, max_stats, absmax_stats]
        return statdicts

    @staticmethod
    def serialize_growth_rates(morph):
        """
        Bundles growth augments for FE5, FE7, FE8, and FE9.
        """
        old_growths = (morph._og_growth_rates * 0.01).as_dict()
        new_growths = (morph.growth_rates * 0.01).as_dict()
        growths_diff = (morph.get_growth_augment() * 0.01).as_dict()
        statdicts = [old_growths, new_growths, growths_diff]
        return statdicts

    @staticmethod
    def serialize_level_up(morph, num_levels: int):
        """
        Bundles level-up stats for FE5, FE7, FE8, and FE9.
        """
        bonus_without_augment = (morph._og_growth_rates * num_levels * 0.01).as_dict()
        augment = (morph.get_growth_augment() * -num_levels * 0.01).as_dict()
        for stat in morph.Stats.ZERO_GROWTH_STAT_LIST():
            bonus_without_augment[stat] = None
            augment[stat] = None
        statdicts = [bonus_without_augment, augment]
        return statdicts
