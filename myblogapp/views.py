from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import BlogPost

# Create your views here.
def blog_feed(request):
    blogposts = BlogPost.objects.filter(published_date__lte=timezone.now())
    return render(request, 'myblogapp/newsfeed.html',{'bps':blogposts})

def view_blogpost(request, pk):
    blogpost = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'myblogapp/blogdetail.html',{'p':blogpost})