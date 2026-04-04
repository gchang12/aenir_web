"""
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

class StatBundle:
    """
    """

    def __init__(self, id: str, current_val: int, growth_rate: int | None, max_val: int, absmax_val: int):
        """
        """
        self.id = id
        self.current_val = current_val / 100
        self.growth_rate = growth_rate
        self.max_val = max_val / 100
        self.absmax_val = absmax_val / 100
