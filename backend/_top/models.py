from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = None
    last_name = None
    email = models.EmailField(
        blank=False,
        primary_key=True,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)
