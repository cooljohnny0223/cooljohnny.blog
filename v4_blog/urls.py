"""v4_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings  # 新增
from django.views.static import serve
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign/', views.sign),  # 註冊
    path('login/', views.login),  # 登入
    path('logout/', views.logout),  # 登出
    path('login/random_code/', views.get_random_code),  # 登入驗證碼
    path('', views.index),  # 首頁
    path('search/', views.search),  # 搜尋

    path('news/', views.news),  # 新聞
    path('moods/', views.moods),  # 心情
    path('history/', views.history),  # 回憶錄
    path('about/', views.about),  # 關於
    path('sites/', views.sites),  # 網站導航

    path('backend/', views.backend),  # 後台個人中心
    path('backend/add_article/', views.add_article),  # 後台添加文章
    path('backend/edit_avatar/', views.edit_avatar),  # 後台修改頭像
    path('backend/reset_password/', views.reset_password),  # 後台修改密碼

    re_path(r'^backend/edit_article/(?P<nid>\d+)/', views.edit_article),  # 後台編輯文章

    # 文章路由配置
    re_path(r'^article/(?P<nid>\d+)/', views.article),  # 文章詳情頁

    # media 路由配置(用戶上傳文件)
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

    # 路由分發  將所有api開頭的請求分發到api這個urls.py中
    re_path(r'^api/', include('api.urls')),
]
