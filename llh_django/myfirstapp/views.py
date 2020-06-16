from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.cache import cache_page
from django import forms
from django.forms import fields
from django.forms import widgets
from myfirstapp import models
import time
import json


# Create your views here.

# error_msg = ''
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
    obj.save()
    print("xxx")

    obj = models.User(user="root")
    obj.save()

    obj = models.User(user="root")
    obj.save()

    return HttpResponse("ok")


# form验证
class FM(forms.Form):
    username = fields.CharField(error_messages={"required": "用户名不能为空！"},
                                label="用户名",
                                )
    password = fields.CharField(max_length=12,
                                min_length=6,
                                label="密码",
                                error_messages=
                                {"required": "密码不能为空！",
                                 "max_length": 12,
                                 "min_length": 6
                                 })
    email = fields.EmailField(error_messages=
    {
        "required": "邮箱不能为空！",
        "invalid": "邮箱格式错误！"
    },
        label="邮箱",
    )


def fm(request):
    if request.method == 'GET':
        obj = FM()
        return render(request, "form.html", {"obj": obj})
    elif request.method == 'POST':
        # 获取用户所有数据
        # 每条数据请求验证
        # 成功：获取所有正确信息
        # 失败：返回错误信息
        obj = FM(request.POST)
        res = obj.is_valid()
        if res:
            # print(obj.cleaned_data)
            models.User.objects.create(**obj.cleaned_data)
        else:
            # print(obj.errors)
            return render(request, "form.html", {"obj": obj})
        return redirect("/fm")
    else:
        return render(request, "form.html")


class FormTestModelForm(forms.ModelForm):
    class Meta:
        model = models.UsersIndex
        fields = "__all__"    # 全部字段
        # fields = ["username", "password", ....]  罗列字段
        # exclude = "username"  排除
        labels = {
            "username": "用户名",
            "password": "密码",
            "email": "邮箱",
            "user_type": "部门",
        }


class FormTest(forms.Form):
    username = fields.CharField(error_messages={"required": "用户名不能为空!"},
                                label="用户名",
                                )
    password = fields.CharField(error_messages={"required": "密码不能为空!"},
                                label="密码"
                                )
    email = fields.EmailField(error_messages={"required": "邮箱不能为空!",
                                              "invalid": "邮箱格式错误！"},
                              label="邮箱"
                              )
    user_type = fields.ChoiceField(
        choices=models.UserType.objects.values_list("id", "caption")
    )

    def __init__(self, *args, **kwargs):
        # 自动更新
        super(FormTest, self).__init__(*args, **kwargs)
        self.fields["user_type"].choices = models.UserType.objects.values_list("id", "caption")


# ModelForm验证
def userIndex(request):
    if request.method == "GET":
        obj = FormTestModelForm()
        return render(request, "modelForm.html", {"obj": obj})
    elif request.method == "POST":
        obj = FormTestModelForm(request.POST)
        if obj.is_valid():
            obj.save()
        # print(obj.is_valid())
        # print(obj.cleaned_data)
        # print(obj.errors)
        return render(request, "modelForm.html", {"obj": obj})


def userList(request):
    li = models.UsersIndex.objects.all().select_related("user_type")
    return render(request, "userList.html", {"li": li})


def userEdit(request, nid):
    if request.method == "GET":
        user_obj = models.UsersIndex.objects.filter(id=nid).first()
        mf = FormTestModelForm(instance=user_obj)
        return render(request, "userEdit.html", {"mf": mf, "nid": nid})
    elif request.method == "POST":
        user_obj = models.UsersIndex.objects.filter(id=nid).first()
        mf = FormTestModelForm(request.POST, instance=user_obj)
        if mf.is_valid():
            mf.save()
        return render(request, "userEdit.html", {"mf": mf, "nid": nid})


def ajax(request):
    return render(request, "ajax.html")

def ajax_json(request):
    print(request.POST)
    ret = {"status": True, "data": None}
    # return HttpResponse(json.dumps(ret), status=404, reason="Not fund")
    return HttpResponse(json.dumps(ret))
