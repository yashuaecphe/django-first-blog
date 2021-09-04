from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_feed, name='blog_newsfeed'),
    path('post/<int:pk>/', views.view_blogpost, name='viewblog'),
]
