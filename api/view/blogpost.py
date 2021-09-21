from rest_framework.permissions import IsAuthenticated
from myblogapp.models import BlogPost
from api.serializers import BlogpostSerializer
from django.http import Http404
from django.utils import timezone

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BlogFeed(APIView): 
    """ api/blogposts/
    For public viewing published blogposts
    """
    def get(self, request, format=None):
        """http http://127.0.0.1:8000/api/blogposts/"""
        blogposts = BlogPost.objects.all().filter(published_date__lte=timezone.now())
        serializer = BlogpostSerializer(blogposts, many=True)
        return Response(serializer.data)

class BlogView(APIView):
    """api/blogpost_view/<int>/
    For public viewing published individual blogposts
    """
    def get(self, request, pk, format=None):
        try:
            serializer = BlogpostSerializer(BlogPost.objects.get(pk=pk))
            return Response(serializer.data)
        except BlogPost.DoesNotExist:
            raise Http404

class BlogCreateOrList(APIView):
    """AUTH api/blogpost_new/
        - create a blogpost
        - view unpublished blogposts
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        serializer = BlogpostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetail(APIView):
    """AUTH api/blogposts/<int>/
       updating or deleting a blogpost
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        serializer = BlogpostSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

