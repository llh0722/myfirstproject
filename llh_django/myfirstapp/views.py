from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page

from myfirstapp import models
import time
# Create your views here.

error_msg = ''
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if obj:
            request.session["username"] = user
            request.session["username"] = True
            if request.POST.get("rmb", None) == "1":
                # 设置超时时间
                request.session.set_expiry(10)
            return redirect('index.html')
        else:
            error_msg = '用户名或密码错误'
            return render(request, 'login.html', {'error_msg': error_msg})
    else:
        return redirect('index.html')

def index(request):
    if request.session["username"]:
        return render(request, 'index.html')
    else:
        return HttpResponse("!!!")

# 注销
def logout(request):
    request.session.clear()
    return redirect("/login/")


# 页面缓存
'''
@cache_page(10)
def cache(request):
    ctime = time.ctime()
    return render(request, "cache.html", {"ctime": ctime})
'''

# 局部缓存

def cache(request):
    ctime = time.ctime()
    return render(request, "cache.html", {"ctime": ctime})

# 全栈缓存  启用中间件


# 信号
def signal(request):
    obj = models.User(user="root")
    print("xxx")
    obj.save()

    obj = models.User(user="root")
    obj.save()

    obj = models.User(user="root")
    obj.save()

    return HttpResponse("ok")
