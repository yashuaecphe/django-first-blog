from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import BlogPost
from .forms import BlogPostForm

# Create your views here.
def blog_feed(request):
    blogposts = BlogPost.objects.filter(published_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'myblogapp/newsfeed.html',{'bps':blogposts, 'is_drafts':False})

def draft_feed(request):
    blogposts = BlogPost.objects.filter(published_date=None)
    return render(request, 'myblogapp/newsfeed.html',{'bps':blogposts, 'is_drafts':True})

def view_blogpost(request, pk):
    blogpost = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'myblogapp/blogdetail.html',{'p':blogpost})

def edit_blogpost(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method=="POST":
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('viewblog',pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
        return render(request, 'myblogapp/blogwriter.html',{'blogform': form})

def save_blogpost_as_draft(request):
    if request.method == "POST": #when you press the submit button for the write form
        form = BlogPostForm(request.POST)
        if form.is_valid(): #true if all fields are filled in
            post = form.save(commit=False) # we dont want to save it yet, we have yet to add an author
            post.author = request.user #who is the user that requested this thing
            #post.published_date = timezone.now()
            post.save()
            return redirect('blog_newsfeed')

    else: #when you click the ADD button
        form = BlogPostForm()
        return render(request, 'myblogapp/blogwriter.html',{'blogform': form})
        #render a form for writing blog

def publish_blogpost(request,pk):
    BlogPost.objects.get(pk=pk).publish()
    return view_blogpost(request,pk)

def delete_blogpost(request,pk):
    BlogPost.objects.get(pk=pk).delete()
    return redirect('blog_newsfeed')