from django.shortcuts import render
from gallery.models import Gallery


def home(request):
    gallerys = Gallery.objects
    return render(request, 'home.html', {'gallerys': gallerys})
