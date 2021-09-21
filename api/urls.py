from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api.view.blogpost import BlogCreateOrList,BlogFeed, BlogDetail, BlogView
from api.view.blogcomment import Comments

urlpatterns = [
    #public list view
    path('blogposts/', BlogFeed.as_view(), name='blogs'),

    #public single view
    path('blogpost_view/<int:pk>/',BlogView.as_view()),

    #AUTH POSTing
    path('blogpost_new/',BlogCreateOrList.as_view()), 
    
    #AUTH PUT or DELETE blogpost 
    path('blogpost/<int:pk>/', BlogDetail.as_view(), name='blog'),

    path('blogpost/<int:pk>/comments/', Comments.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)