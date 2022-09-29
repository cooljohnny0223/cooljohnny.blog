from django import template
from app01.utils.search import Search  # 導入自定義的搜尋方法
from django.utils.safestring import mark_safe  # 安全放入html語法
from app01.models import Tags  # 標籤資料

# 註冊
register = template.Library()


# 自定義過濾器-數值加1
# @register.filter
# def add1(item):
#     return item + 1

# 首頁輪播圖片
@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    # 圖片列表
    img_list = [
        "/static/my/img/nav/bg1.jpg",
        "/static/my/img/nav/bg2.jpg",
        "/static/my/img/nav/bg3.jpg",
    ]

    # 文章詳細頁面
    if article:
        # 說明是文章詳情頁面
        # 拿到文章的封面
        cover = article.cover.url.url
        img_list = [cover]
        pass

    # {"img_list": img_list}  --> 使用字典方式傳遞資料
    return {"img_list": img_list}


# 搜尋
@register.simple_tag
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('-change_date', '默認排序'),
            ('-create_date', '最新發佈'),
            ('-look_count', '最多瀏覽'),
            ('-digg_count', '最多點讚'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多評論')
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        order_list = [
            ([''], '全部字數'),
            (['0', '100'], '100字以內'),
            (['100', '500'], '500字以內'),
            (['500', '1000'], '1000字以內'),
            (['1000', '3000'], '3000字以內'),
            (['3000', '5000'], '5000字以內')
        ]
    elif key == 'tag':
        # 取得資料庫 標籤的內容並且判斷是否標籤下有文章  exclude 篩選掉滿足的條件
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部標籤'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))
    query_params = request.GET.copy()
    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())


# 顯示對應的圖標和數字(遺漏)

# 生成標籤(遺漏)

# 動態導航
@register.simple_tag
def dynamic_navigation(request):
    path = request.path_info
    path_dict = {
        '/': '首頁',
        '/news/': '新聞',
        '/moods/': '心情',
        '/history/': '回憶錄',
        '/about/': '關於',
        '/sites/': '網站導航',
    }
    nav_list = []
    for k, v in path_dict.items():
        if k == path:
            nav_list.append(f'<a href="{k}" class="active">{v}</a>')
            continue
        nav_list.append(f'<a href="{k}">{v}</a>')
    return mark_safe(''.join(nav_list))


# 生成廣告
@register.simple_tag
def generate_advert(advert_list):
    html_list = []
    for i in advert_list:
        if i.img:
            # 上傳的圖片
            html_list.append(
                f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{i.img.url}"></a></div>')
            continue
        html_s: str = i.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')
        for url in img_list:
            html_list.append(
                f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{url}"></a></div>')
    return mark_safe(''.join(html_list))
