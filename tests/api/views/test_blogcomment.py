from api.views.blogcomment import BlogCommentsAPI
from django.contrib.auth.models import User
from django.utils import timezone
from myblogapp.models import BlogComment, BlogPost
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

class TestBlogcomments(APITestCase):
    """testing /api/blogpost/<int>/comments/ endpoint."""
    
    def setUp(self)->None:
        """To test the BlogCommentsAPI, we will need:
        - 2 testusers
        - 2 test blogpost both owned by one of the testuser
            one published and one unpublished
        - 2 comments for the first blogpost, one approved, the other unapproved
        """
        self.factory = APIRequestFactory()
        self.view = BlogCommentsAPI.as_view()
        self.api_path = '/api/blogpost/<int:pk>/comments/'

        # if test user wasn't deleted previously (like test interrupted), delete it
        testuser = User.objects.filter(username='testuser')
        while len(testuser) > 0: testuser[0].delete()
        #create a superuser
        self.testuser = User.objects.create_user(username='testuser', password='testpass', is_superuser=True, is_staff=True)
        self.testuser.save()

        # if test user wasn't deleted previously (like test interrupted), delete it
        testuser = User.objects.filter(username='testuser2')
        while len(testuser) > 0: testuser[0].delete()
        #create a superuser
        self.testuser2 = User.objects.create_user(username='testuser2', password='testpass', is_superuser=True, is_staff=True)
        self.testuser2.save()

        #create test blogposts to test later
        self.published_blogpost_test = BlogPost.objects.create(author=self.testuser, title="published_blogpost_title",text="published_blogpost_text", published_date=timezone.now())
        self.unpublished_blogpost_test = BlogPost.objects.create(author=self.testuser, title="unpublished_blogpost_title", text="unpublished_blogpost_text")   

        # comments under the published_blogpost_test
        self.approved_comment_test = BlogComment.objects.create(author="testcommenter", post=self.published_blogpost_test.id, text="test comment that is approved", approved=True)
        self.pending_comment_test = BlogComment.objects.create(author="testcommenter2",post=self.published_blogpost_test.id, text="this comment is pending for approval")

    def test_viewing_comments_OWNER(self)->None:
        """viewing the comments of a blogpost as the owner of that blogpost
            the author can view all comments approved or unapproved
        """
        pass

    def test_viewing_comments_AUTH(self)->None:
        """viewing the comments of a blogpost as someone else
            can only view approved comments
        """
        pass

    def test_viewing_comments_no_auth(self)->None:
        """viewing the comments no authorization
            can only view approved comments
        """
        pass