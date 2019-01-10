from django.shortcuts import render


def index(req):
    """首页函数"""
    return render(req, 'index.html', locals())