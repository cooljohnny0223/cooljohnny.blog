import random
from django.views import View
from django.http import JsonResponse
from markdown import markdown  # 解析Markdown資料至html內容
from pyquery import PyQuery  # 解析html內容資料
from app01.models import Tags, Articles, Cover
from django import forms
from api.views.login import clean_form
from django.db.models import F


# 添加文章或編輯文章表單字段驗證
class AddArticleForm(forms.Form):
    # 字段內容
    title = forms.CharField(error_messages={'required': '請輸入文章標題'})
    content = forms.CharField(error_messages={'required': '請輸入文章內容'})
    abstract = forms.CharField(required=False)  # 不進行空驗證
    cover_id = forms.IntegerField(required=False)  # 不進行空驗證
    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    # 全局勾子-驗證分類和文章密碼
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    # 文章簡介
    def clean_abstract(self):
        abstrace = self.cleaned_data['abstract']
        if abstrace:
            return abstrace
        # 截取正文的前90個字符
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        # 未選擇，默認隨機選擇一張封面
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id


# 給文章添加標籤
def add_article_tags(tags, article_obj):
    for tag in tags:
        if tag.isdigit():
            article_obj.tag.add(tag)
        else:
            # 先創建在，再多對多關聯
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)


# 文章請求視圖
class ArticleView(View):
    # 添加文章
    def post(self, request):
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '文章發佈成功！！',
            'data': None,
        }
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        # 驗證不通過
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 驗證通過
        # 添加文章
        form.cleaned_data['author'] = '尚豪'
        form.cleaned_data['source'] = '尚豪部落格'
        article_obj = Articles.objects.create(**form.cleaned_data)
        # 標籤新增
        tags = data.get('tags')
        add_article_tags(tags, article_obj)
        # 添加成功
        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 編輯文章
    def put(self, request, nid):
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '文章修改成功！！',
            'data': None,
        }
        # 找不到文章, 返回請求錯誤訊息
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '請求錯誤！'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        # 驗證不通過
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 驗證通過
        # 添加文章
        form.cleaned_data['author'] = '尚豪'
        form.cleaned_data['source'] = '尚豪部落格'
        # 更新資料
        article_query.update(**form.cleaned_data)
        # 標籤修改
        tags = data.get('tags')
        article_query.first().tag.clear()  # 清空所有標籤
        add_article_tags(tags, article_query.first())
        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)


# 文章點讚
class ArticleDiggView(View):
    def post(self, request, nid):
        # nid 評論id
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '文章點讚成功！！',
            'data': 0,
        }
        # 必須登入才能點讚
        if not request.user.username:
            res['msg'] = '請先登入再點讚！'
            res['self'] = 'content'
            return JsonResponse(res)

        # 文章點讚 +1
        article_query = Articles.objects.filter(nid=nid)
        article_query.update(digg_count=F('digg_count') + 1)

        digg_count = article_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)


# 文章收藏
class ArticleCollectsView(View):
    def post(self, request, nid):
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '文章收藏成功！！',
            'isCollects': True,  # 是否是收藏
            'data': 0,
        }
        # 必須登入才能收藏
        if not request.user.username:
            res['msg'] = '請先登入再收藏！'
            res['self'] = 'content'
            return JsonResponse(res)
        # 同樣的請求，收藏變取消收藏
        # 判斷用戶是否收藏過文章
        flag = request.user.collects.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:
            # 用戶已經收藏了文章，取消收藏
            res['msg'] = '文章取消收藏成功！'
            res['isCollects']: False
            request.user.collects.remove(nid)
            # 文章收藏數-1
            num = -1
        else:
            # 用戶文章收藏
            request.user.collects.add(nid)

        # 文章收藏數 +1 或 -1
        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)
        collects_count = article_query.first().collects_count
        res['data'] = collects_count

        return JsonResponse(res)
