from django import forms
from django.contrib import auth
from app01.models import UserInfo, Avatars
from django.views import View
from django.http import JsonResponse
import random


# 登入基本表單字段驗證
class LoginBaseForm(forms.Form):
    # 字段內容
    name = forms.CharField(error_messages={'required': '請輸入用戶名！'})
    pwd = forms.CharField(error_messages={'required': '請輸入密碼！'})
    code = forms.CharField(error_messages={'required': '請輸入驗證碼！'})

    # 重寫init方法
    def __init__(self, *args, **kwargs):
        # 做自己想要做的事情
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # 「局部鈎子」-驗證碼核對

    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        valid_code: str = self.request.session.get('valid_code')
        # 全部轉換成大寫來核對驗證碼
        if valid_code.upper() != code.upper():
            self.add_error('code', '驗證碼輸入錯誤！')
        return self.cleaned_data


# 登入的字段驗證
class LoginForm(LoginBaseForm):
    # 「全局鈎子」-校驗用戶名和密碼
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        # 獲得user對象
        user = auth.authenticate(username=name, password=pwd)
        if not user:
            self.add_error('pwd', '用戶名或密碼錯誤')  # 為字段添加錯誤訊息
            return self.cleaned_data

        # 把用戶對象放到clean_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data


# 註冊的字段驗證
class SignForm(LoginBaseForm):
    # 字段內容
    re_pwd = forms.CharField(error_messages={'required': '請輸入確認密碼！'})

    # 「全局鈎子」-密碼與確認密碼是否相同
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '兩次密碼不一致')
        return self.cleaned_data

    # 「局部鈎子」-校驗用戶名不可以重覆
    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '該用戶名已註冊！')
        return self.cleaned_data


# 登入失敗的可復用的程式碼
def clean_form(form):
    err_dict: dict = form.errors
    # 拿到所有錯誤字段名字
    err_valid = list(err_dict.keys())[0]
    # 拿到第一個字段的第一個錯誤信息
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg


# 登入
class LoginView(View):
    def post(self, request):
        # 返回給前端的資料
        res = {
            'code': 425,
            'msg': '登入成功！',
            'self': None,
        }
        form = LoginForm(request.data, request=request)
        # 驗證不通過
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 登入成功
        user = (form.cleaned_data.get('user'))
        auth.login(request, user)  # 登入操作
        res['code'] = 0
        return JsonResponse(res)


# 註冊
class SignView(View):
    def post(self, request):
        # 返回給前端的資料
        res = {
            'code': 425,
            'msg': '註冊成功！',
            'self': None,
        }
        form = SignForm(request.data, request=request)
        if not form.is_valid():
            # 驗證不通過
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 註冊成功
        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('pwd')
        )
        # 隨機選擇頭像 (使用列表生成式)
        avatar_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_list)
        user.save()

        auth.login(request, user)  # 註冊之後直接登入
        res['code'] = 0
        return JsonResponse(res)
