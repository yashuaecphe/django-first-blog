from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_feed, name='blog_newsfeed'), #normal news feed
    path('drafts', views.draft_feed, name='draft_newsfeed'),
    path('blogpost/<int:pk>/', views.view_blogpost, name='viewblog'),
    path('write', views.save_blogpost_as_draft, name='write_blogpost' ),
    path('editblogpost/<int:pk>', views.edit_blogpost,name='editblog'),
    path('publishblogpost/<int:pk>', views.publish_blogpost, name='publishblog'),
    path('deleteblog/<int:pk>', views.delete_blogpost, name='deleteblog')
]
