from myblogapp.models import BlogComment, BlogPost
from api.serializers import BlogcommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Comments(APIView):
    """comments api endpoint
        - GET list of comments
        - POST a comment
    """
    def get_blogpost(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        bp = self.get_blogpost(pk)
        comments = BlogComment.objects.filter(post=bp)
        serializer = BlogcommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        serializer = BlogcommentSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    