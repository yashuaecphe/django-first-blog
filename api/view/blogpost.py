from myblogapp.models import BlogPost
from api.serializers import BlogpostSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BlogFeed(APIView):
    """List of BlogPosts or create a new blogpost"""

    def get(self, request, format=None):
        """http http://127.0.0.1:8000/api/blogposts/"""
        blogposts = BlogPost.objects.all()
        serializer = BlogpostSerializer(blogposts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """api endpoint: 
        http --form POST http://127.0.0.1:8000/api/blogposts/ author=1, ... other fields
        """
        serializer = BlogpostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogDetail(APIView):
    """ GET, PUT, or DELETE blog instance"""

    def get_object(self,pk):
        """called by other functions how do i private doe"""
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        """http http://127.0.0.1:8000/api/blogposts/<int>/"""
        serializer = BlogpostSerializer(self.get_object(pk))
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        """http PUT http:127.0.0.1:8000/api/blogposts/<int>/ the=required fields=value"""
        serializer = BlogpostSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        """http DELETE http://127.0.0.1:8000/api/blogposts/<int>/"""
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
