from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_feed, name='blog_newsfeed'),
    path('blogpost/<int:pk>/', views.view_blogpost, name='viewblog'),
    path('write', views.write_blogpost, name='write_blogpost' ),
    path('editblogpost/<int:pk>', views.edit_blogpost,name='editblog'),
]
