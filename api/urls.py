from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.view.blogpost import BlogFeed, BlogDetail

urlpatterns = [
    path('blogposts/', BlogFeed.as_view()),
    path('blogposts/<int:pk>/', BlogDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)