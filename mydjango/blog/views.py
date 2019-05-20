from django.shortcuts import render, get_object_or_404
from . import models
# Create your views here.


def blog_page(request):
    blogs = models.Blog.objects
    return render(request, 'blog.html', {'blogs': blogs})


def blog_text(request, blog_id):  # blog_id 作为参数被传递到这个函数里所以要接收
    blog = get_object_or_404(models.Blog, pk=blog_id)
    return render(request, 'blog_text.html', {'blog': blog})
