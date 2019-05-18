from django.shortcuts import render
from . import models
# Create your views here.


def blog_page(request):
    blogs = models.Blog.objects
    return render(request, 'blog.html', {'blogs': blogs})
