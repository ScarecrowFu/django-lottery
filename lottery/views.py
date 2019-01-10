from django.shortcuts import render
from django.shortcuts import render, HttpResponse
import json
from lottery.models import User


def index(req):
    # 首页初始化
    value = ['一等奖', '二等奖']
    return render(req, 'index.html', locals())


def get_all_users(req):
    # 取得所有参与抽奖的用户
    users = []
    for user in User.objects.all():
        users.append(user.name)
    return HttpResponse(json.dumps({"success": True, "users": users}), content_type="application/json")