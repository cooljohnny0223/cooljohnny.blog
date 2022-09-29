from django import template

register = template.Library()


# 自定義過濾器-判斷用戶是否收藏文章
@register.filter
def is_user_collects(article, request):
    if str(request.user) == 'AnonymousUser':
        # 沒有登入
        return ''
    if article in request.user.collects.all():
        # 有收藏顯示樣式
        return 'show'
    # 沒有收藏
    return ''


# 判斷是否有文章內容
@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'
