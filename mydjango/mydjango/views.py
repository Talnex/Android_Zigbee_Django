import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from gallery.models import UploadImage
from blog.models import Blog
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
            return HttpResponse(person.name)
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
        Person.objects.create(name=name, password=password, email=email)
        return HttpResponse('success')
    else:
        return HttpResponse('用户名已存在')

@csrf_exempt
def myadmin(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            print("已认证")
            users = Person.objects
            return render(request, "usercontrol.html", {"users": users})
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = auth.authenticate(request, username=username, password=password)
            if user:
                auth.login(request, user)
                users = Person.objects
                blogs = Blog.objects
                print("成功")
                return render(request, "usercontrol.html", {"users": users,"blogs":blogs,"user":user})
            else:
                print("失败")
                return render(request, "myadmin.html")
    else:
        print("访问")
        return render(request, "myadmin.html")


@csrf_exempt
@login_required
def delate_user(request):
    userid = request.POST.get('userid')
    status = "删除成功"
    result = "Error!"
    deletesql = Person.objects.filter(id=userid)
    if deletesql.delete():
        return HttpResponse(json.dumps({
            "status": status
        }))
    else:
        return HttpResponse(json.dumps({
            "result": result
        }))


@csrf_exempt
@login_required
def delate_blog(request):
    blogid = request.POST.get('blogid')
    status = "删除成功"
    result = "Error!"
    deletesql = Blog.objects.filter(id=blogid)
    if deletesql.delete():
        return HttpResponse(json.dumps({
            "status": status
        }))
    else:
        return HttpResponse(json.dumps({
            "result": result
        }))

@csrf_exempt
def change_user(request):
    email = request.POST.get('email')
    name = request.POST.get('name')
    password = request.POST.get('password')
    person = Person.objects.get(email=email)
    person.name = name
    person.password = password
    person.save()
    return HttpResponse('success')