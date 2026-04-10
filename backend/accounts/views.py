"""
"""

from django import forms
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    BaseUserCreationForm,
    #UserCreationForm,
    UsernameField,
)

User = get_user_model()

class CreateAccountView(CreateView):
    """
    """
    class UserCreationForm(BaseUserCreationForm):
        """
        """
        class Meta(BaseUserCreationForm.Meta):
            """
            """
            model = User
            fields = ("username", "email")
            field_classes = {
                "username": UsernameField,
                "email": forms.EmailField,
            }
    template_name = "registration/create_account.html"
    form_class = UserCreationForm
    success_url = "/accounts/login/"

class ProfileView(TemplateView):
    #class ProfileView(UpdateView):
    """
    """
    template_name = "accounts/profile.html"
