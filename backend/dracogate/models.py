"""
"""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

# User
# ArenaTeam
# Morph

class Deadlords(models.Model):
    """
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Morph(models.Model):
    """
    """
    id = models.CharField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadlords = models.ManyToManyField(to=Deadlords)
    history = models.JSONField()
