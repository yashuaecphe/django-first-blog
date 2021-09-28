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
        self.approved_comment_test = BlogComment.objects.create(author="testcommenter", post=self.published_blogpost_test, text="test comment that is approved", approved_comment=True)
        self.approved_comment_test_dict = {   
                "approved_comment":self.approved_comment_test.approved_comment,
                "author":self.approved_comment_test.author,
                "created_date": str(self.approved_comment_test.created_date)[:10],
                "post":self.approved_comment_test.post.id,
                "text":self.approved_comment_test.text,
            }

        self.pending_comment_test = BlogComment.objects.create(author="testcommenter2",post=self.published_blogpost_test, text="this comment is pending for approval")
        self.pending_comment_test_dict = { 
                "approved_comment":self.pending_comment_test.approved_comment,
                "author":self.pending_comment_test.author,
                "created_date":str(self.pending_comment_test.created_date)[:10],
                "post":self.pending_comment_test.post.id,
                "text":self.pending_comment_test.text
            }

    def test_viewing_comments_OWNER(self)->None:
        """viewing the comments of a blogpost as the owner of that blogpost
            the author can view all comments approved or unapproved
        """
        expected_response_data = [self.approved_comment_test_dict, self.pending_comment_test_dict,]

        request = self.factory.get(self.api_path)
        force_authenticate(request, user=self.testuser)
        response = self.view(request, pk=self.published_blogpost_test.id)

        #only base the YYYY-MM-DD on the date because tests have second-differences
        for rd in response.data:
            rd["created_date"] = rd["created_date"][:10]

        self.assertEqual(response.status_code, 200)
        for i in range(0,len(expected_response_data)):
            for k in expected_response_data[i].keys():
                self.assertEqual(response.data[i][k], expected_response_data[i][k])
        

    def test_viewing_comments_AUTH(self)->None:
        """viewing the comments of a blogpost as someone else
            can only view approved comments
        """
        expected_response_data = [self.approved_comment_test_dict]

        request = self.factory.get(self.api_path)
        force_authenticate(request, user=self.testuser2)
        response = self.view(request, pk=self.published_blogpost_test.id)
        
        for rd in response.data:
            rd["created_date"] = rd["created_date"][:10]
        
        self.assertEqual(response.status_code, 200)
        for i in range(0,len(expected_response_data)):
            for k in expected_response_data[i].keys():
                self.assertEqual(response.data[i][k], expected_response_data[i][k])

    def test_viewing_comments_no_auth(self)->None:
        """viewing the comments no authorization
            can only view approved comments
            responds same as AUTH
        """
        expected_response_data = [self.approved_comment_test_dict]

        request = self.factory.get(self.api_path)
        response = self.view(request, pk=self.published_blogpost_test.id)
        
        for rd in response.data:
            rd["created_date"] = rd["created_date"][:10]
        
        self.assertEqual(response.status_code, 200)
        for i in range(0,len(expected_response_data)):
            for k in expected_response_data[i].keys():
                self.assertEqual(response.data[i][k], expected_response_data[i][k])
        
    def test_viewing_comments_of_unpublished_blogpost(self)->None:
        """viewing the comments of a blogpost that isn't published
            doesn't matter if owner, authorized, or public, it will return an error
            since you can't comment on an unpublished blogpost (test for that below)
        """
        expected_response_data = {"detail":"This post is unpublished."}

        request = self.factory.get(self.api_path)
        force_authenticate(request, user=self.testuser)
        response = self.view(request, pk=self.unpublished_blogpost_test.id)
        
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, expected_response_data)

    def test_post_comment_published_blogpost(self)->None:
        """commenting on a published blogpost
            whether OWNER, AUTH, or public, results are the same
        """
        data_comment = {
            "author":"SEx Master",
            "post": self.published_blogpost_test.id,
            "text": "greetings, I am a certified SEx doer",
            "approved_comment": True, #testing this exploit where clients can force comment approval
        }

        request = self.factory.post(self.api_path, data_comment)
        response = self.view(request, pk=self.published_blogpost_test.id)

        self.assertEqual(response.status_code, 201)
        #self.assertEqual(response.data["author"], data_comment["author"])
        for i in ["author","text","post"]:
            self.assertEqual(response.data[i] ,data_comment[i])
        self.assertEqual(response.data["approved_comment"], False)
    
    def test_post_comment_unpublished_blogpost(self)->None:
        """comment on an unpublished blogpost
            whether OWNER, AUTH or public, results are the same
        """
        expected_response_data = {"detail":"This post is unpublished."}
        data_comment = {
            "author":"doge",
            "post": self.published_blogpost_test.id,
            "text": "don't google scientifig name for pig",
        }

        request = self.factory.post(self.api_path, data_comment)
        response = self.view(request, pk=self.unpublished_blogpost_test.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, expected_response_data)
    
    def test_post_comment_nonexistent_post(self)->None:
        """posting a comment to a blogpost that doesn't exist"""
        expected_response_data = {"detail":"Not found."}
        request = self.factory.post(self.api_path, {})
        response = self.view(request, pk=0)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_response_data)
