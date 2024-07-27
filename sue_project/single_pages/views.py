from django.shortcuts import render
from blog.models import Post

def landing(request):
    recent_posts = Post.objects.order_by('-time')[:3]
    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html',
    )

def Login(request):
    return render(
        request,
        'single_pages/Login.html'
    )