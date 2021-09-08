from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_feed, name='blog_newsfeed'), #normal news feed
    path('drafts', views.draft_feed, name='draft_newsfeed'), #draft news feed
    path('blogpost/<int:pk>/', views.view_blogpost, name='viewblog'), #view a singular blog
    path('write', views.save_blogpost_as_draft, name='write_blogpost' ), #write a blog
    path('editblogpost/<int:pk>', views.edit_blogpost,name='editblog'), #edit a blog
    path('publishblogpost/<int:pk>', views.publish_blogpost, name='publishblog'), #publish a blog
    path('deleteblog/<int:pk>', views.delete_blogpost, name='deleteblog'), #delete a blog
    path('blogpost/<int:pk>/comment', views.add_comment_to_blogpost, name='add_comment_to_blogpost'),
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),  
]
