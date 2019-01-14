"""django_lottery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url, include
from lottery.views import index, get_all_users, get_prize_by_class, get_all_prizes, lottery, get_winner_users, reset_all, reset_by_prize

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url(r'^index/$', index, name='index'),  # 首页
                  url(r'^get_all_users/$', get_all_users, name='get_all_users'),
                  url(r'^get_prize_by_class/$', get_prize_by_class, name='get_prize_by_class'),
                  url(r'^get_all_prizes/$', get_all_prizes, name='get_all_prizes'),
                  url(r'^lottery/$', lottery, name='lottery'),
                  url(r'^get_winner_users/$', get_winner_users, name='get_winner_users'),
                  url(r'^reset_all/$', reset_all, name='reset_all'),
                  url(r'^reset_by_prize/$', reset_by_prize, name='reset_by_prize'),
                  url(r'^$', index, name='index'),  # 首页
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
