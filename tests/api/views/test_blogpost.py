from api.views.blogpost import BlogPostAPI, BlogPostsAPI
from django.db.models import DateTimeField
from django.utils import timezone
from django.contrib.auth.models import User
from myblogapp.models import BlogPost
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate

class TestBlogposts(APITestCase):
    """testing api/blogposts."""
    
    def setUp(self)->None:
        # if test user wasn't deleted previously (like test interrupted), delete it
        testuser = User.objects.filter(username='testuser')
        if len(testuser) > 0: testuser[0].delete()
        #create a superuser
        self.testuser = User.objects.create_user(username='testuser', password='testpass', is_superuser=True, is_staff=True)
        self.testuser.save()

        self.factory = APIRequestFactory()
        self.view = BlogPostsAPI.as_view()
        self.api_path = '/api/blogposts/'

    def test_get_blogposts_public_access(self)->None:
        """if GET and no authorization, should return a list of published posts"""
        query_published = BlogPost.objects.filter(published_date__lte=timezone.now())
        
        expected_titles = [ q.title for q in query_published ]
        expected_texts = [ q.text for q in query_published ]
        expected_published_dates = [ q.published_date for q in query_published ]
        expected_created_dates = [ q.created_date for q in query_published ]
        expected_authors = [ q.author for q in query_published ] 

        request = self.factory.get(self.api_path)
        response = self.view(request)

        response_titles = [ r["title"] for r in response.data ]
        response_texts = [ r["text"] for r in response.data ]
        response_published_dates = [ r["published_date"] for r in response.data ]
        response_created_dates = [ r["created_date"] for r in response.data ]
        response_authors = [ r["author"] for r in response.data ]

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response_titles, expected_titles)
        self.assertQuerysetEqual(response_texts, expected_texts)
        self.assertQuerysetEqual(response_published_dates, expected_published_dates)
        self.assertQuerysetEqual(response_created_dates, expected_created_dates)
        self.assertQuerysetEqual(response_authors, expected_authors)
        
    def test_posting_new_blogpost_authorized(self)->None:
        """testing POST with authorization."""
        data = {'author':self.testuser.id,
                'title':'test_posting_new_blogpost_authorized', 
                'text':'this post is made by TestBlogposts.test_posting_new_blogpost_authorized() from tests.api.views.test_blogposts'}

        expected_author = self.testuser.id
        expected_title = data["title"]
        expected_text = data["text"]
        expected_created_date = str(timezone.now())

        request = self.factory.post(self.api_path, data)
        force_authenticate(request, user=self.testuser)
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], expected_author)
        self.assertEqual(response.data['title'], expected_title)
        self.assertEqual(response.data["text"], expected_text)
        #self.assertEqual(response.data["created_date"], expected_created_date)

    def test_posting_new_blogpost_unauthorized(self)->None:
        """testing POST unauthorized."""
        expected_response_data = {'detail':'Authentication required'}
        request = self.factory.post(self.api_path, data={}) #data is irrelevant for this case
        response = self.view(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, expected_response_data)