from myblogapp.models import BlogComment, BlogPost
from api.serializers import BlogcommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BlogCommentsAPI(APIView):
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
        """returns a list of APPROVED comments if public access
            list of all comments if the user is the owner of that blogpost
        """
        bp = self.get_blogpost(pk)
        if bp.published_date is None: #unpublished
            return Response(data={"detail":"This post is unpublished."}, status=status.HTTP_403_FORBIDDEN)

        comments = BlogComment.objects.filter(post=bp)
        if (not request.user.is_authenticated) or (request.user!=bp.author): # not the user
            comments = comments.filter(approved_comment=True)
            
        serializer = BlogcommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, format=None):
        """adds a comment
            shouldn't be able to add a comment to a blogpost that is unpublished
        """
        if self.get_blogpost(pk).published_date is None: #unpublished post
            return Response(data={"detail":"This post is unpublished."}, status=status.HTTP_403_FORBIDDEN)
        serializer = BlogcommentSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.validated_data["approved_comment"] = False #to prevent client-forced approval
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    