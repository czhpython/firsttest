from django.shortcuts import render
from LoginApp.models import LoginUser
from django.http import HttpResponseRedirect

"""
拓展功能：
    1、密码加密
        注册加密
        登陆需要加密
    2、cookie校验编写装饰器
    3、cookie和session进行混合校验
    4、用户名重复不可以注册
        1、后端校验
        2、ajax前端校验
"""

def index(request):
    username = request.COOKIES.get("username")
    if username:
        user = LoginUser.objects.filter(username=username).first()
        if user:
            return render(request,"index.html")
    return HttpResponseRedirect("/login/")

def register(request):
    result = {"content":""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = LoginUser()
            user.username = username
            user.password = password
            user.save()
            return HttpResponseRedirect("/login/")
        else:
            result["content"] = "用户名或者密码不可以为空"
    return render(request,"register.html",locals())

def login(request):
    result = {"content": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = LoginUser.objects.filter(username = username).first()
            if user:
                if password == user.password:
                    response = HttpResponseRedirect("/index/")
                    response.set_cookie("username",user.username)
                    return response
                else:
                    result["content"] = "密码错误"
            else:
                result["content"] = "用户名不存在"
        else:
            result["content"] = "用户名或密码不可以为空"
    return render(request,"login.html",locals())

def logout(request):
    response = HttpResponseRedirect("/login/")
    response.delete_cookie("username")
    return response
# Create your views here.
