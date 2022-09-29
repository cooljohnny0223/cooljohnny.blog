from django.utils.deprecation import MiddlewareMixin
import json


# 解析post請求的數據
class Md1(MiddlewareMixin):
    # 請求中間件
    def process_request(self, request):
        # 判斷不是「Get請求」且為「application/json」 才進行處理，避免Django後台出錯
        if request.method != 'GET' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)
            request.data = data

    # 響應中間件
    def process_response(self, request, response):
        return response
