from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from myfirstapp import models
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


