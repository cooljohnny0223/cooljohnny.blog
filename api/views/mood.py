from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django.db.models import F
from django import forms
from app01.models import Avatars, Moods, MoodComment
import random


# 發佈心情表單字段驗證
class AddMoodsForm(forms.Form):
    # 字段內容
    name = forms.CharField(error_messages={'required': '請輸入用戶名'})
    content = forms.CharField(error_messages={'required': '請輸入心情內容'})
    avatar_id = forms.CharField(required=False)  # 不進行為空驗證
    drawing = forms.CharField(required=False)  # 不進行為空驗證

    def clean_avatar_id(self):
        avatar_id = self.cleaned_data.get('avatar_id')
        if avatar_id:
            return avatar_id
        # 隨機選擇頭像
        avatar_list = [ i.nid for i in Avatars.objects.all()]
        avatar_id = random.choice(avatar_list)
        return avatar_id


# 發佈心情
class MoodsView(View):
    def post(self, request):
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '心情發佈成功！！',
            'self': None,
        }
        data = request.data
        form = AddMoodsForm(data)
        # 驗證不通過
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        Moods.objects.create(**form.cleaned_data)

        res['code'] = 0
        return JsonResponse(res)
