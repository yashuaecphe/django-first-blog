from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.view.blogpost import BlogFeed, BlogDetail
from api.view.blogcomment import Comments

urlpatterns = [
    path('blogposts/', BlogFeed.as_view()), # GET list of blogposts or POST a new one
    path('blogpost/<int:pk>/', BlogDetail.as_view()), #GET, PUT, or DELETE a single blogpost
    path('blogpost/<int:pk>/comments/', Comments.as_view()), #GET list of comments from a certain blogpost, or create a new one

]

urlpatterns = format_suffix_patterns(urlpatterns)