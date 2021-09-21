from django.contrib.auth.models import User
from rest_framework import serializers
from myblogapp.models import BlogComment, BlogPost

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    blogposts = serializers.PrimaryKeyRelatedField(many=True, queryset=BlogPost.objects.all())

    class Meta:
        model = User
        fields = ['url','blogposts','author']
    
class BlogpostSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.author')

    class Meta:
        model = BlogPost
        fields = ['author','title','text','created_date','published_date']

class BlogcommentSerializer(serializers.ModelSerializer):
    #post = serializers.HyperlinkedRelatedField(view_name='blog', read_only=True)
    class Meta:
        model = BlogComment
        fields = ['author','post','text','created_date','approved_comment']
