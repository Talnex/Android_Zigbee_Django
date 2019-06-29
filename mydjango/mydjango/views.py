from django.shortcuts import render
from gallery.models import UploadImage
from blog.models import Person
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt



def home(request):
    gallerys = UploadImage.objects
    return render(request, 'home.html', {'gallerys': gallerys})


@csrf_exempt
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        person = Person.objects.get(email=email)
    except ObjectDoesNotExist:
        return HttpResponse('用户不存在')
    else:
        if person.password == password:
            return HttpResponse("success")
        else:
            return HttpResponse('密码错误')

@csrf_exempt
def signup(request):
    name = request.POST.get('name')
    password = request.POST.get('password')
    email = request.POST.get('email')

    try:
        Person.objects.get(email=email)
    except ObjectDoesNotExist:
        Person.objects.create(name=name,password=password,email=email)
        return HttpResponse('success')
    else:
        return HttpResponse

