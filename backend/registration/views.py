"""
"""

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

User = get_user_model()

class CreateAccountView(CreateView):
    """
    """
    model = User
    #fields = ["email", "username", "password"]
    fields = ["email", "password"]
    template_name = "registration/create_account.html"
    success_url = "/accounts/login/"

    def get(self, request, *args, **kwargs):
        """
        """
        response = super().get(request, *args, **kwargs)
        print("request.user", request.user)
        print("dir(request.session)", dir(request.session))
        print("request.session.session_key", request.session.session_key)
        #print("request.auth", request.auth)
        return response
