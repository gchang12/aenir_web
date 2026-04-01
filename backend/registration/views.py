"""
"""

from django.shortcuts import render
from django.contrib.auth import (
    get_user_model,
    logout,
)
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView

from rest_framework import (
    viewsets,
    views,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import (
    Response,
)

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

class UsernameViewSet(viewsets.ViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        """
        """
        username = request.user.email
        return Response({
            "username": username,
        })

class LogoutView(viewsets.ViewSet):
    """
    """
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
        """
        print("request", request)
        print("request.session", request.session)
        print("request.user", request.user)
        logout(request)
        print("request.user", request.user)
        return Response()
