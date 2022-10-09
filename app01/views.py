from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code  # 導入自定義的驗證碼方法
from django.contrib import auth
from app01.models import UserInfo
from app01.models import *
from app01.utils.sub_comment_list import sub_comment_list  # 導入自定義的子評論清單方法
from app01.utils.pagination import Pagination  # 導入自定義的分頁器方法
from django.db.models import F


# 註冊
def sign(request):
    return render(request, 'sign.html')


# 登入
def login(request):
    return render(request, 'login.html')


# 獲取隨機驗證碼
def get_random_code(request):
    data, valid_code = random_code()  # 獲取驗證碼
    request.session['valid_code'] = valid_code  # 驗證碼，「存入」到session內
    return HttpResponse(data)


# 首頁
def index(request):
    # 獲得所有(已發佈)的文章內容 ordery_by('-create_date')遞減排序 ('create_date')遞增排序
    article_list = Articles.objects.filter(status=1).order_by('-create_date')
    # 精選文章-前端、後端 (只顯示6篇文章)
    forward_list = article_list.filter(category=1)[:6]
    back_list = article_list.filter(category=2)[:6]

    # print(article_list)

    # 分頁
    query_params = request.GET.copy()
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10,
        pager_page_count=7,
    )
    article_list = article_list[pager.start:pager.end]

    # 廣告
    advert_list = Advert.objects.filter(is_show=True)

    return render(request, 'index.html', locals())


# 自定義標籤-搜尋條件
def search(request):
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    word = request.GET.getlist('word', '')
    tag = request.GET.get('tag', '')

    query_params = request.GET.copy()

    article_list = Articles.objects.filter(title__contains=search_key).order_by('-change_date')
    if len(word) == 2:
        article_list = article_list.filter(word__range=word)
    if tag:
        article_list = article_list.filter(tag__title=tag)

    if order:
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass
    # 分頁
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=5,  # 每頁顯示筆數
        pager_page_count=7,  # 最大分頁數
    )
    article_list = article_list[pager.start:pager.end]

    # 文章搜尋條件
    query_params.urlencode()

    return render(request, 'search.html', locals())


# 文章詳情頁
def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    # 增加瀏覽次數
    article_query.update(look_count=F('look_count') + 1)
    # 查找不到文章nid，則返回首頁
    if not article_query:
        return redirect('/')
    article = article_query.first()  # 取得文章
    comment_list = sub_comment_list(nid)  # 評論清單
    return render(request, 'article.html', locals())


# 新聞
def news(request):
    return render(request, 'news.html')


# 心情
def moods(request):
    # 查詢所有的頭像
    avatar_list = Avatars.objects.all()
    mood_list = Moods.objects.all()
    return render(request, 'moods.html', locals())


# 回憶錄
def history(request):
    return render(request, 'history.html')


# 關於
def about(request):
    return render(request, 'about.html')


# 網站導航
def sites(request):
    return render(request, 'sites.html')


# 登出
def logout(request):
    auth.logout(request)
    return redirect('/')


# ========[後台區]========

# 後台-個人中心
def backend(request):
    # 沒有登入，直接回到首頁
    if not request.user.username:
        return redirect('/')
    return render(request, 'backend/backend.html', locals())


# 後台-添加文章
def add_article(request):
    # 拿到所有文章分類
    category_list = Articles.category_choice
    # 拿到所有標籤
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    # 為了前端頁面取得隨機封面資料
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid,
        })
    return render(request, 'backend/add_article.html', locals())


# 後台-編輯文章
def edit_article(request, nid):
    # 使用get好處，可以直接返回對象 fillter，還需要使用first()才能夠返回對象
    article_obj = Articles.objects.get(nid=nid)
    # 標籤序列化-取得選中的
    tags = [str(tag.nid) for tag in article_obj.tag.all()]

    # 拿到所有文章分類
    category_list = Articles.category_choice
    # 拿到所有標籤
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    # 為了前端頁面取得隨機封面資料
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid,
        })
    return render(request, 'backend/edit_article.html', locals())


# 後台-修改頭像
def edit_avatar(request):
    return render(request, 'backend/edit_avatar.html', locals())


# 後台-修改密碼
def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())
