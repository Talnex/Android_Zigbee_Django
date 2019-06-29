"""mydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import gallery.views
from . import views
import blog.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    # path('blog/', blog.views.blog_page)
    path("upload/blog",blog.views.uploadBlog),
    path("upload/image", gallery.views.uploadImage),
    path('blog/', include('blog.urls')),
    path('login', views.login),
    path('signup', views.signup),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
