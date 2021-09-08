# put your forms here

from django import forms
from .models import BlogPost, BlogComment

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title','text',)

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ('author','text',)