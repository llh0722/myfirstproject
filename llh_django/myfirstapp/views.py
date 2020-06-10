from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from myfirstapp import models
# Create your views here.

def login(request):
    # error_msg = ''
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        obj = models.UserInfo.objects.filter(username=user, password=pwd).first()
        if obj:
            return redirect('index.html')
        else:
            error_msg = '用户名或密码错误'
            return render(request, 'login.html', {'error_msg': error_msg})
    else:
        return redirect('index.html')

def index(request):
    return render(request, 'index.html')

