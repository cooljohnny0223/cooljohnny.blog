from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.db.models.signals import pre_delete  # 刪除文件
from django.dispatch.dispatcher import receiver  # 刪除文件


# 網站信息表
class Site(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='網站標題')
    abstract = models.CharField(max_length=128, verbose_name='網站簡介')
    key_words = models.CharField(max_length=128, verbose_name='網站關鍵字')
    record = models.CharField(max_length=32, verbose_name='網站備案號')
    create_date = models.DateTimeField(verbose_name='建站日期')
    version = models.CharField(max_length=16, verbose_name='網站版本號')
    icon = models.FileField(verbose_name='網站圖示', upload_to='site_icon/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '網站信息'  # 後端顯示表名


# 個人信息
class MyInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name='名字')
    job = models.CharField(max_length=128, verbose_name='工作')
    email = models.EmailField(max_length=64, verbose_name='電子信箱')
    site_url = models.CharField(max_length=32, verbose_name='網站連結')
    addr = models.CharField(max_length=16, verbose_name='地址')
    bilbili_url = models.URLField(verbose_name='嗶哩嗶哩連接')
    github_url = models.URLField(verbose_name='GitHub連接')
    wechat_img = models.FileField(verbose_name='微信圖片', upload_to='my_info/')
    qq_img = models.FileField(verbose_name='QQ圖片', upload_to='my_info/')

    class Meta:
        verbose_name_plural = '個人信息'


# 用戶表
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    sign_choice = (
        (0, '用戶名註冊'),
        (1, '手機註冊'),
        (2, '郵箱註冊'),
        (3, 'QQ註冊'),
    )
    name = models.CharField(max_length=16, verbose_name='暱稱')
    sign_status = models.IntegerField(default=8, verbose_name='註冊方式')
    tel = models.CharField(max_length=10, verbose_name='手機')
    integral = models.IntegerField(default=20, verbose_name='用戶積分')
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='用戶頭像',
        null=True
    )
    collects = models.ManyToManyField(
        to='Articles',
        verbose_name='收藏的文章',
        blank=True
    )

    class Meta:
        verbose_name_plural = '用戶'


# 用戶頭像表
class Avatars(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='用戶頭像地址', upload_to='avatars/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '用戶頭像'


@receiver(pre_delete, sender=Avatars)  # sender=你要刪除或修改文件字段所在的類**
def download_delete(instance, **kwargs):  # 函數名隨意
    # print('進入文件刪除方法，刪的是', instance.url) # 用於測試
    instance.url.delete(False)  # file是保存文件或圖片的字段名**


# 文章表
class Articles(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='標題', null=True, blank=True)
    abstract = models.CharField(max_length=128, verbose_name='文章簡介', null=True, blank=True)
    content = models.TextField(verbose_name='文章內容', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name='文章發佈日期', auto_now_add=True, null=True)
    change_date = models.DateTimeField(verbose_name='文章修改日期', auto_now=True, null=True)
    status_choice = (
        (0, '未發佈'),
        (1, '已發佈'),
    )
    status = models.IntegerField(verbose_name='文章保存狀態', choices=status_choice)
    recommend = models.BooleanField(verbose_name='是否上推薦', default=True)
    cover = models.ForeignKey(
        to='Cover',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='文章幫面', null=True, blank=True
    )
    look_count = models.IntegerField(verbose_name='文章閱讀量', default=0)
    comment_count = models.IntegerField(verbose_name='文章評論量', default=0)
    digg_count = models.IntegerField(verbose_name='文章點讚量', default=0)
    collects_count = models.IntegerField(verbose_name='文章收藏數', default=0)
    category_choice = (
        (1, '前端'),
        (2, '後端'),
        (3, '項目相關'),
    )
    category = models.IntegerField(verbose_name='文章分類', choices=category_choice, null=True, blank=True)
    tag = models.ManyToManyField(
        to='Tags',
        verbose_name='文章標籤',
        blank=True
    )
    pwd = models.CharField(max_length=32, verbose_name='文章密碼', null=True, blank=True)
    author = models.CharField(max_length=16, verbose_name='作者', null=True, blank=True)
    source = models.CharField(max_length=32, verbose_name='來源', null=True, blank=True)
    link = models.URLField(verbose_name='文章連結', null=True, blank=True)
    word = models.IntegerField(verbose_name='文章字數', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章'


# 評論表
class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    digg_count = models.IntegerField(verbose_name='點讚', default=0)
    article = models.ForeignKey(verbose_name='評論文章', to='Articles', to_field='nid', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='評論者', to='UserInfo', to_field='nid', on_delete=models.CASCADE, null=True)
    content = models.TextField(verbose_name='評論內容')
    comment_count = models.IntegerField(verbose_name='子評論數', default=0)
    drawing = models.TextField(verbose_name='配圖', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='創建時間', auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name='是否是父評論')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '評論'


# 新聞的爬取記錄
class New(models.Model):
    nid = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(verbose_name='獲取時間', auto_now_add=True)

    class Meta:
        verbose_name_plural = '新聞爬取'


# 文章封面
class Cover(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='文章封面地址', upload_to='article_img/')

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = '文章封面'


@receiver(pre_delete, sender=Cover)  # sender=你要刪除或修改文件字段所在的類**
def cover_delete(instance, **kwargs):  # 函數名隨意
    # print('進入文件刪除方法，刪的是', instance.url) # 用於測試
    instance.url.delete(False)  # file是保存文件或圖片的字段名**


# 標籤表
class Tags(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16, verbose_name='標籤名字')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章標籤'


# 回憶錄
class History(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='事件名稱')
    content = models.TextField(verbose_name='事件內容')
    create_date = models.DateTimeField(verbose_name='發佈時間', auto_now_add=True)
    drawing = models.TextField(verbose_name='配圖組，以;隔開', null=True, blank=True)

    class Meta:
        verbose_name_plural = '回憶錄'


# 心情
class Moods(models.Model):
    nid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=16, verbose_name='發佈人')
    ip = models.GenericIPAddressField(verbose_name='IP地址', default='114.33.106.143')
    addr = models.JSONField(verbose_name='用戶地址信息', null=True)
    create_date = models.DateTimeField(verbose_name='發佈時間', auto_now_add=True)
    content = models.TextField(verbose_name='心情內容')
    drawing = models.TextField(verbose_name='配圖組，以;隔開', null=True, blank=True)
    comment_count = models.IntegerField(verbose_name='評論數', default=0)
    digg_count = models.IntegerField(verbose_name='點讚數', default=0)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='心情的發佈頭像',
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '心情'


# 心情評論
class MoodComment(models.Model):
    nid = models.AutoField(primary_key=True)
    avatar = models.ForeignKey(
        to='Avatars',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='心情的發佈頭像',
        null=True
    )
    name = models.CharField(verbose_name='評論人', max_length=16, null=True)
    content = models.TextField(verbose_name='評論內容')
    digg_count = models.IntegerField(verbose_name='點讚數', default=0)
    ip = models.GenericIPAddressField(verbose_name='IP地址', default='114.33.106.143')
    addr = models.JSONField(verbose_name='用戶地址信息', null=True)
    mood = models.ForeignKey(
        to='Moods',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='評論的心情',
        null=True
    )
    create_date = models.DateTimeField(verbose_name='評論時間', auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '心情評論'


# 網站導航
class Navs(models.Model):
    nid = models.AutoField(primary_key=True)
    nav_category = models.ForeignKey(
        to='NavCategory',
        to_field='nid',
        on_delete=models.SET_NULL,
        verbose_name='網站導航的分類',
        null=True
    )
    icon_href = models.URLField(verbose_name='團隊連接', help_text='在線連接', null=True, blank=True)
    icon = models.FileField(
        verbose_name='網站圖標', null=True, blank=True,
        upload_to='site_icon/', help_text='文件優先級大於在線連接'
    )
    title = models.CharField(max_length=32, verbose_name='網站標題')
    abstract = models.CharField(max_length=128, verbose_name='網站簡介', null=True)
    create_date = models.DateTimeField(verbose_name='創建時間', auto_now=True)
    href = models.URLField(verbose_name='網站連接')
    status_choice = (
        (0, '待審核'),
        (1, '已審核'),
        (2, '被駁回'),
    )
    status = models.IntegerField(verbose_name='導航狀態', choices=status_choice, default=0)

    def color_state(self):
        if self.status == 0:
            assign_state_name = '待審核'
            color_code = '#ec921e'
        elif self.status == 1:
            assign_state_name = '已通過'
            color_code = 'green'
        else:
            assign_state_name = '已駁回'
            color_code = 'red'
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code,
            assign_state_name,
        )

    color_state.short_description = '導航狀態'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '網站導航'


# 導航分類
class NavCategory(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=16, verbose_name='分類標題')
    icon = models.CharField(max_length=32, verbose_name='分類圖標')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '導航分類'


# 站點背景
class Menu(models.Model):
    nid = models.AutoField(primary_key=True)
    menu_title = models.CharField(max_length=16, verbose_name='菜單名稱', null=True)
    menu_title_en = models.CharField(max_length=32, verbose_name='菜單英文名稱', null=True)
    title = models.CharField(max_length=32, verbose_name='slogan', null=True)
    abstract = models.TextField(verbose_name='slogan介紹', help_text='多個之間按分號區分', null=True)
    abstract_item = models.IntegerField(verbose_name='slogan切換時間', help_text='單位秒，默認是8秒', default=8)
    rotation = models.BooleanField(verbose_name='是否輪播slogan介紹', default=True)
    menu_url = models.ManyToManyField(
        to='MenuImg',
        verbose_name='菜單圖片',
        help_text='可以多選，多選就會輪播',
    )
    menu_ratation = models.BooleanField(verbose_name='是否輪播banner圖', help_text='多選默認會輪播', default=False)
    menu_time = models.IntegerField(verbose_name='背景圖切換時間', help_text='單位秒，默認是8秒', default=8)

    class Meta:
        verbose_name_plural = "站點背景"


# 站點背景
class MenuImg(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.FileField(verbose_name='圖片地址', upload_to='site_bg/')

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = '站點背景圖'


# 廣告表
class Advert(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32, verbose_name='廣告名稱', null=True)
    href = models.URLField(verbose_name='跳轉連接')
    img = models.FileField(verbose_name='圖片地址', null=True, blank=True, help_text='單圖', upload_to='advert/')
    img_list = models.TextField(verbose_name='圖片組', null=True, blank=True, help_text='上傳圖片請用線上地址，使用；隔開多張圖片')
    is_show = models.BooleanField(verbose_name='是否展示', default=False)
    author = models.CharField(max_length=32, verbose_name='廣告主', null=True, blank=True)
    abstract = models.CharField(max_length=128, verbose_name='產品簡介', null=True, blank=True)

    class Meta:
        verbose_name_plural = '廣告'


# 反饋信息
class Feedback(models.Model):
    nid = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='電子信箱')
    content = models.TextField(verbose_name='反饋信息')
    stats = models.BooleanField(verbose_name='是否處理', default=False)
    processing_content = models.TextField(verbose_name='回復的內容', null=True, blank=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '用戶反饋'
