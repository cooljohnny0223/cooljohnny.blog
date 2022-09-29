from django.contrib import admin
# from app01.models import Articles  # 文章表
# from app01.models import Tags  # 標籤表
# from app01.models import Cover  # 文章封面表
# from app01.models import Comment  # 文章評論表
# from app01.models import UserInfo  # 用戶
# from app01.models import Avatars  # 頭像
from app01.models import *
from django.utils.safestring import mark_safe


# 文章表
class ArticleAdmin(admin.ModelAdmin):
    # 顯示文章封面
    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="width:160px; height:100px; border-radius:5px;">')
        return

    get_cover.short_description = '文章封面'

    # 顯示標籤
    def get_tag(self):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list

        # 尾部會多一個,
        # tag_html=""
        # for tag in self.tag.all():
        #     tag_html += tag.title + ','

    get_tag.short_description = '標籤'

    # 自訂文章標題 連結到文章詳情頁
    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}/" target="_blank">{self.title}</a>')

    get_title.short_description = '標題'

    # 操作按鈕「編輯」、「刪除」
    def get_edit_delete_btn(self):
        return mark_safe(f"""
        <a href="/backend/edit_article/{self.nid}/" target="_blank">編輯</a>
        <a href="/admin/app01/articles/{self.nid}/delete/">刪除</a>
        """)

    list_display = [get_title, get_cover, get_tag, 'category', 'look_count', 'digg_count', 'comment_count',
                    'collects_count', 'word', 'change_date', get_edit_delete_btn]
    get_edit_delete_btn.short_description = '操作'

    # 自訂義執行動作-獲取文章字數
    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_word.short_description = '獲取文章字數'
    action_word.type = 'success'
    actions = [action_word]


admin.site.register(Articles, ArticleAdmin)

# 用戶信息表
admin.site.register(UserInfo)


# 廣告表
class AdvertAdmin(admin.ModelAdmin):
    def get_href(self):
        return mark_safe(f"""<a href="{self.href}" target="_blank">跳轉連結</a>""")

    get_href.short_description = '跳連連結'

    def get_img_list(self):
        # 解析分號;
        # 解析換行符號\n
        html_s: str = self.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')

        html_str = ''
        for i in img_list:
            html_str += f'<img src="{i}" style="height:60px; border-radius:5px; margin-right:10px">'
        return mark_safe(html_str)

    get_img_list.short_description = '廣告圖片組'

    def get_img(self):
        # 注意點：要判斷有沒有值，不然會報錯
        if self.img:
            return mark_safe(f"""<img src="{self.img.url}" style="height:60px; border-radius:5px;">""")

    get_img.short_description = '圖片地址'

    list_display = ['title', get_img, 'is_show', 'author', get_img_list, get_href]

admin.site.register(Advert, AdvertAdmin)

admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
