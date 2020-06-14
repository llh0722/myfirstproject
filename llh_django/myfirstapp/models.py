from django.db import models

# Create your models here.
# python manage.py makemigrations  将类转换成数据表结构
# python manage.py  migrate  根据上一句代码生成数据表


# 创建用户组表
class UserGroup(models.Model):
    uid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=32, unique=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)
    update_time = models.DateTimeField(auto_now=True, null=True)


# 创建用户表
class UserInfo(models.Model):
    # 创建用户名列
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64, null=True)
    # test = models.EmailField(max_length=64, null=True,
    #                          error_messages={"invalid": "请输入密码！"})
    # 创建外键
    user_group = models.ForeignKey("UserGroup", to_field='uid', default=1, on_delete=models.CASCADE)
    user_type_choices = (
        (1, "超级用户"),
        (2, "VIP用户"),
        (3, "普通用户"),
    )
    user_type_id = models.IntegerField(choices=user_type_choices, default=1)

class User(models.Model):
    user = models.CharField(max_length=32)

class UserType(models.Model):
    caption = models.CharField(max_length=32)

class UsersInfo(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField()
    user_type = models.ForeignKey(to_field="id", to="UserType", on_delete=models.CASCADE)
