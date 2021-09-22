
from api.serializers import BlogpostSerializer
from django.http import Http404, Http403
from django.utils import timezone
from myblogapp.models import BlogPost
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class BlogList(APIView): 
    """ api/blogposts/
        - GET list of (AUTH optional)
            if authenticated: list of all blogposts by the user (even unpublished ones)
            else: list of all published blogposts
        - POST a new blogpost (AUTH required)
            the request.user will become the author
    """
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_authenticated:
            # if authenticated, will return all the posts of the user
            blogposts = BlogPost.objects.all().filter(author=request.user.id)
            serializer = BlogpostSerializer(blogposts, many=True)
            return Response(serializer.data)
        else:
            # if not, will return all published posts
            blogposts = BlogPost.objects.all().filter(published_date__lte=timezone.now())
            serializer = BlogpostSerializer(blogposts, many=True)
            return Response(serializer.data)
    
    def post(self, request, format=None):
        if request.user.is_authenticated: # AUTH REQUIRED
            serializer = BlogpostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data["author"] = request.user
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: #otherwise return error
            return Response({"detail":"Authentication required"}, status.HTTP_401_UNAUTHORIZED)


class BlogDetail(APIView):
    """api/blogpost/<int>/
       - GET a single blogpost
            anyone can access any published post
            but only the author can access their unpublished posts
       - PUT update a single blogpost (AUTH required)
            requires authentication and that the user should be the author of that post
            the request.user will be the author of that post
       - DELETE a single blogpost (AUTH required)
            requires authentication and that the user should be the author of that post
    """
    def get_object(self,pk)->BlogPost:
        try: return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist: raise Http404
    
    def get(self, request, pk, format=None):
        blogpost = self.get_object(pk)
        serializer = BlogpostSerializer(blogpost)
        if (blogpost.published_date is None) and (request.user!=blogpost.author): #post is unpublished
            #return Response(data={"detail":"You are not authorized to view this unpublished post"},status=status.HTTP_403_FORBIDDEN)
            raise Http403
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        owner_of_postdelete = self.get_object(pk).author
        if request.user==owner_of_postdelete:
            #authorized user is the author of the post
            #the author will be the user
            serializer = BlogpostSerializer(self.get_object(pk), data=request.data)
            if serializer.is_valid():
                serializer.validated_data["author"] = request.user
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={"detail":"You are not authorized to PUT this blogpost"}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk, format=None):
        owner_of_postdelete = self.get_object(pk).author
        if request.user==owner_of_postdelete:
            #authorized user is the author of the post
            self.get_object(pk).delete()
            return Response(data={"detail":f"Deleted post {pk} successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"detail":"You are not authorized to DELETE this blogpost"}, status=status.HTTP_403_FORBIDDEN)
