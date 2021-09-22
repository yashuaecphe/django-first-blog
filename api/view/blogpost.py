
from api.serializers import BlogpostSerializer
from django.http import Http404
from django.utils import timezone
from myblogapp.models import BlogPost
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions


class BlogList(APIView): 
    """ api/blogposts/
        - GET list of
            if authenticated: list of all blogposts by the user (even unpublished)
            else: list of all published blogposts
        - POST a new blogpost (REQUIRES AUTH)
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
        if request.user.is_authenticated:
            serializer = BlogpostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"Authentication required"}, status.HTTP_401_UNAUTHORIZED)


    

class BlogDetail(APIView):
    """api/blogpost/<int>/
       - GET a single blogpost
       - PUT update a single blogpost
       - DELETE a single blogpost
    """
    def get_object(self,pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        serializer = BlogpostSerializer(self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        serializer = BlogpostSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

