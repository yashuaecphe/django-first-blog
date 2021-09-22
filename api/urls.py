
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns

from api.view.blogpost import BlogList, BlogDetail
from api.view.blogcomment import Comments
from api.view.auth import AuthView

urlpatterns = [
    path('blogposts/', BlogList.as_view(), name='blogs'),
    path('blogpost/<int:pk>/', BlogDetail.as_view(), name='blog'),
    path('blogpost/<int:pk>/comments/', Comments.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', create_auth_token)
]

urlpatterns = format_suffix_patterns(urlpatterns)