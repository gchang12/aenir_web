"""
"""

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

User = get_user_model()

class CreateAccountView(CreateView):
    model = User
    fields = ["username", "password"]
    template_name = "registration/create_account.html"
    success_url = "http://localhost:3000/"
