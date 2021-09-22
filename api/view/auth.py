from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import Token
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth.models import User

class AuthView(APIView):
    def get(self, request, format=None):
        """Return a list of users."""
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


