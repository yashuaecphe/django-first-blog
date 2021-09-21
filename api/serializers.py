from django.contrib.auth.models import User
from rest_framework import serializers
from myblogapp.models import BlogComment, BlogPost

class AuthorSerializer(serializers.ModelSerializer):
    blogposts = serializers.PrimaryKeyRelatedField(many=True, queryset=BlogPost.objects.all())

    class Meta:
        model = User
        fields = ['url','blogposts','author']
    
class BlogpostSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.author')

    class Meta:
        model = BlogPost
        fields = ['author','title','text','created_date','published_date']



