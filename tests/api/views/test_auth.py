from api.views.auth import UserList, ObtainAuthenticationToken
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory

class TestOAuth(APITestCase):

    def setUp(self)->None:
        # if test user wasn't deleted previously (like test interrupted), delete it
        testuser = User.objects.filter(username='testuser')
        if len(testuser) > 0: testuser[0].delete()

        #create a superuser
        self.testuser = User.objects.create_user(username='testuser', password='testpass', is_superuser=True, is_staff=True)
        self.testuser.save()

        self.factory = APIRequestFactory()
        self.api_path = 'api/obtain-token/'
        self.view = ObtainAuthenticationToken.as_view()

    def test_obtaining_token_with_right_credentials(self)->None:
        """testing api/obtain-token/ with correct credentials."""
        expected_user = self.testuser
        expected_token = Token.objects.get_or_create(user=expected_user)[0]
        request = self.factory.post(self.api_path, {'username':'testuser','password':'testpass'})
        response = self.view(request)

        recieved_token = response.data["token"]
        recieved_username = response.data["user"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(recieved_token),str(expected_token))
        self.assertEqual(recieved_username, expected_user.username)

    def test_obtaining_token_with_wrong_credentials(self)->None:
        """testing api/obtain-token/ with wrong credentials"""
        expected_user = self.testuser
        expected_token = Token.objects.get_or_create(user=expected_user)[0]
        request = self.factory.post(self.api_path, {'username':'nonexistent','password':'nonexistent'})
        response = self.view(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["message"],"Invalid username/password")





