
from api.serializers import BlogpostSerializer
from django.http import Http404
from django.utils import timezone
from myblogapp.models import BlogPost

from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BlogList(APIView): 
    """ api/blogposts/
        - GET list of all published blogposts
        - POST a new blogpost (REQUIRES AUTH)
    """
    def get(self, request, format=None):
        blogposts = BlogPost.objects.all().filter(published_date__lte=timezone.now())
        serializer = BlogpostSerializer(blogposts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BlogpostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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

