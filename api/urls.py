
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns

from api.views.blogpost import BlogPostsAPI, BlogPostAPI
from api.views.blogcomment import Comments
from api.views.auth import UserList, ObtainAuthenticationToken

urlpatterns = [
    path('blogposts/', BlogPostsAPI.as_view(), name='blogs'),
    path('blogpost/<int:pk>/', BlogPostAPI.as_view(), name='blog'),
    path('blogpost/<int:pk>/comments/', Comments.as_view()),
    path('obtain-token/', ObtainAuthenticationToken.as_view()),
    path('api-auth/', UserList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)