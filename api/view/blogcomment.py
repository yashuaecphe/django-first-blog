from myblogapp.models import BlogComment, BlogPost
from api.serializers import BlogcommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Comments(APIView):
    """
    /api/blogpost/<int:pk>/comments/
        For getting list of comments at a certain blogpost or making a new comment. 
    """

    def get_blogpost(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        bp = self.get_blogpost(pk)
        comments = BlogComment.objects.filter(post=bp)
        if (not request.user.is_authenticated) or (request.user!=bp.author):
            comments = comments.filter(approved_comment=True)
        serializer = BlogcommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk, format=None):
        serializer = BlogcommentSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    