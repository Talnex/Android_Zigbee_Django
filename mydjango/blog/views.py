from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from gallery.views import returnOk
from . import models
import markdown
from django.conf import settings


# Create your views here.


def blog_page(request):
    blogs = models.Blog.objects
    return render(request, 'blog.html', {'blogs': blogs})


def blog_text(request, blog_id):  # blog_id 作为参数被传递到这个函数里所以要接收
    blog = get_object_or_404(models.Blog, pk=blog_id)
    blog.text = markdown.markdown(blog.text,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'mdx_math'
                                  ])
    return render(request, 'blog_text.html', {'blog': blog})

@csrf_exempt
def uploadBlog(request):
    blog = models.Blog()
    blog.text = request.POST.get('text')
    blog.title = request.POST.get('title')
    blog.author = request.POST.get('author')
    blog.image = request.FILES.get('img')
    blog.save()
    return returnOk({"url": settings.WEB_HOST_NAME +'/'+ str(blog.id)})
