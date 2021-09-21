from myblogapp.models import BlogComment, BlogPost
from api.serializers import BlogcommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class Comments(APIView):
    """GET comment list of a certain post, or POST comment to a certain post"""
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

    #def post(self,request,pk,format=None):pass