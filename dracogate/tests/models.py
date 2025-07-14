from django.test import TestCase

# Create your tests here.

from dracogate.models import (
    Morph4,
    Morph5,
    Morph6,
    Morph7,
    Morph8,
    Morph9,
)
from dracogate._logging import logger

class MorphTests(TestCase):
    """
    """

    def setUp(self):
        """
        """
        logger.debug("%s", self.id())

    def test_something(self):
        """
        """
