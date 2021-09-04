from django.shortcuts import render
from django.utils import timezone
from .models import BlogPost

# Create your views here.
def blog_feed(request):
    blogposts = BlogPost.objects.filter(published_date__lte=timezone.now())
    return render(request, 'myblogapp/newsfeed.html',{'bps':blogposts})

