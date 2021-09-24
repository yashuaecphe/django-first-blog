from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import Token
from rest_framework.authtoken.views import ObtainAuthToken


class UserList(APIView):
    """List all Users."""

    def get(self, request, format=None):
        """Return a list of users."""
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class ObtainAuthenticationToken(ObtainAuthToken):
    """Generate Token for the user param."""

    def post(self, request, *args, **kwargs):
        """ POST user for user parameters
            but this won't save anything, it will simply generate the user's tokens and return it. 
        """
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={
                'token': token.key,
                'user': request.data['username']
            })
        except:
            return Response(data={'message':'Invalid username/password'},status=401)