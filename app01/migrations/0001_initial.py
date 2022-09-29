# Generated by Django 4.1 on 2022-08-28 03:11

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, verbose_name='暱稱')),
                ('sign_status', models.IntegerField(default=8, verbose_name='註冊方式')),
                ('tel', models.CharField(max_length=10, verbose_name='手機')),
                ('integral', models.IntegerField(default=20, verbose_name='用戶積分')),
            ],
            options={
                'verbose_name_plural': '用戶',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, null=True, verbose_name='廣告名稱')),
                ('href', models.URLField(verbose_name='跳轉連接')),
                ('img', models.FileField(blank=True, help_text='單圖', null=True, upload_to='advert/', verbose_name='圖片地址')),
                ('img_list', models.TextField(blank=True, help_text='上傳圖片請用線上地址，使用；隔開多張圖片', null=True, verbose_name='圖片組')),
                ('is_show', models.BooleanField(default=False, verbose_name='是否展示')),
                ('author', models.CharField(blank=True, max_length=32, null=True, verbose_name='廣告主')),
                ('abstract', models.CharField(blank=True, max_length=128, null=True, verbose_name='產品簡介')),
            ],
            options={
                'verbose_name_plural': '廣告',
            },
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=32, null=True, verbose_name='標題')),
                ('abstract', models.CharField(blank=True, max_length=128, null=True, verbose_name='文章簡介')),
                ('content', models.TextField(blank=True, null=True, verbose_name='文章內容')),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='文章發佈日期')),
                ('change_date', models.DateTimeField(auto_now=True, null=True, verbose_name='文章修改日期')),
                ('status', models.IntegerField(choices=[(0, '未發佈'), (0, '已發佈')], verbose_name='文章保存狀態')),
                ('recommend', models.BooleanField(default=True, verbose_name='是否上推薦')),
                ('look_count', models.IntegerField(default=0, verbose_name='文章閱讀量')),
                ('comment_count', models.IntegerField(default=0, verbose_name='文章評論量')),
                ('digg_count', models.IntegerField(default=0, verbose_name='文章點讚量')),
                ('collects_count', models.IntegerField(default=0, verbose_name='文章收藏數')),
                ('category', models.IntegerField(blank=True, choices=[(0, '前端'), (1, '後端')], null=True, verbose_name='文章分類')),
                ('author', models.CharField(blank=True, max_length=16, null=True, verbose_name='作者')),
                ('source', models.CharField(blank=True, max_length=32, null=True, verbose_name='來源')),
            ],
            options={
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Avatars',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.FileField(upload_to='avatars/', verbose_name='用戶頭像地址')),
            ],
            options={
                'verbose_name_plural': '用戶頭像',
            },
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.FileField(upload_to='article_img/', verbose_name='文章封面地址')),
            ],
            options={
                'verbose_name_plural': '文章封面',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, verbose_name='電子信箱')),
                ('content', models.TextField(verbose_name='反饋信息')),
                ('stats', models.BooleanField(default=False, verbose_name='是否處理')),
                ('processing_content', models.TextField(blank=True, null=True, verbose_name='回復的內容')),
            ],
            options={
                'verbose_name_plural': '用戶反饋',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='事件名稱')),
                ('content', models.TextField(verbose_name='事件內容')),
                ('create_date', models.DateField(null=True, verbose_name='創建時間')),
                ('drawing', models.TextField(blank=True, null=True, verbose_name='配圖組，以;隔開')),
            ],
            options={
                'verbose_name_plural': '回憶錄',
            },
        ),
        migrations.CreateModel(
            name='MenuImg',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.FileField(upload_to='site_bg/', verbose_name='圖片地址')),
            ],
            options={
                'verbose_name_plural': '站點背景圖',
            },
        ),
        migrations.CreateModel(
            name='MyInfo',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32, verbose_name='名字')),
                ('job', models.CharField(max_length=128, verbose_name='工作')),
                ('email', models.EmailField(max_length=64, verbose_name='電子信箱')),
                ('site_url', models.CharField(max_length=32, verbose_name='網站連結')),
                ('addr', models.CharField(max_length=16, verbose_name='地址')),
                ('bilbili_url', models.URLField(verbose_name='嗶哩嗶哩連接')),
                ('github_url', models.URLField(verbose_name='GitHub連接')),
                ('wechat_img', models.FileField(upload_to='my_info/', verbose_name='微信圖片')),
                ('qq_img', models.FileField(upload_to='my_info/', verbose_name='QQ圖片')),
            ],
            options={
                'verbose_name_plural': '個人信息',
            },
        ),
        migrations.CreateModel(
            name='NavCategory',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=16, verbose_name='分類標題')),
                ('icon', models.CharField(max_length=32, verbose_name='分類圖標')),
            ],
            options={
                'verbose_name_plural': '導航分類',
            },
        ),
        migrations.CreateModel(
            name='New',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='獲取時間')),
            ],
            options={
                'verbose_name_plural': '新聞爬取',
            },
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=32, verbose_name='網站標題')),
                ('abstract', models.CharField(max_length=128, verbose_name='網站簡介')),
                ('key_words', models.CharField(max_length=128, verbose_name='網站關鍵字')),
                ('record', models.CharField(max_length=32, verbose_name='網站備案號')),
                ('create_date', models.DateTimeField(verbose_name='建站日期')),
                ('version', models.CharField(max_length=16, verbose_name='網站版本號')),
                ('icon', models.FileField(upload_to='site_icon/', verbose_name='網站圖示')),
            ],
            options={
                'verbose_name_plural': '網站信息',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=16, verbose_name='標籤名字')),
            ],
            options={
                'verbose_name_plural': '文章標籤',
            },
        ),
        migrations.CreateModel(
            name='Navs',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('icon_href', models.URLField(blank=True, help_text='在線連接', null=True, verbose_name='團隊連接')),
                ('icon', models.FileField(blank=True, help_text='文件優先級大於在線連接', null=True, upload_to='site_icon/', verbose_name='網站圖標')),
                ('title', models.CharField(max_length=32, verbose_name='網站標題')),
                ('abstract', models.CharField(max_length=128, null=True, verbose_name='網站簡介')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='創建時間')),
                ('href', models.URLField(verbose_name='網站連接')),
                ('status', models.IntegerField(choices=[(0, '待審核'), (1, '已審核'), (2, '被駁回')], default=0, verbose_name='導航狀態')),
                ('nav_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.navcategory', verbose_name='網站導航的分類')),
            ],
            options={
                'verbose_name_plural': '網站導航',
            },
        ),
        migrations.CreateModel(
            name='Moods',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, verbose_name='發佈人')),
                ('create_date', models.DateField(null=True, verbose_name='發佈時間')),
                ('content', models.TextField(verbose_name='心情內容')),
                ('drawing', models.TextField(blank=True, null=True, verbose_name='配圖組，以;隔開')),
                ('comment_count', models.IntegerField(default=0, verbose_name='評論數')),
                ('digg_count', models.IntegerField(default=0, verbose_name='點讚數')),
                ('avatar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.avatars', verbose_name='心情的發佈頭像')),
            ],
            options={
                'verbose_name_plural': '心情',
            },
        ),
        migrations.CreateModel(
            name='MoodComment',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16, null=True, verbose_name='評論人')),
                ('content', models.TextField(verbose_name='評論內容')),
                ('digg_count', models.IntegerField(default=0, verbose_name='點讚數')),
                ('create_date', models.DateTimeField(auto_now=True, verbose_name='評論時間')),
                ('avatar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.avatars', verbose_name='心情的發佈頭像')),
                ('mood', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.moods', verbose_name='評論的心情')),
            ],
            options={
                'verbose_name_plural': '心情評論',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('menu_title', models.CharField(max_length=16, null=True, verbose_name='菜單名稱')),
                ('menu_title_en', models.CharField(max_length=32, null=True, verbose_name='菜單英文名稱')),
                ('title', models.CharField(max_length=32, null=True, verbose_name='slogan')),
                ('abstract', models.TextField(help_text='多個之間按分號區分', null=True, verbose_name='slogan介紹')),
                ('abstract_item', models.IntegerField(default=8, help_text='單位秒，默認是8秒', verbose_name='slogan切換時間')),
                ('rotation', models.BooleanField(default=True, verbose_name='是否輪播slogan介紹')),
                ('menu_ratation', models.BooleanField(default=False, help_text='多選默認會輪播', verbose_name='是否輪播banner圖')),
                ('menu_time', models.IntegerField(default=8, help_text='單位秒，默認是8秒', verbose_name='背景圖切換時間')),
                ('menu_url', models.ManyToManyField(help_text='可以多選，多選就會輪播', to='app01.menuimg', verbose_name='菜單圖片')),
            ],
            options={
                'verbose_name_plural': '站點背景',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('digg_count', models.IntegerField(default=0, verbose_name='點讚')),
                ('content', models.TextField(verbose_name='評論內容')),
                ('comment_count', models.IntegerField(default=0, verbose_name='子評論數')),
                ('drawing', models.TextField(blank=True, null=True, verbose_name='配圖')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='創建時間')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.articles', verbose_name='評論文章')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.comment', verbose_name='是否是父評論')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='評論者')),
            ],
            options={
                'verbose_name_plural': '評論',
            },
        ),
        migrations.AddField(
            model_name='articles',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.cover', verbose_name='文章幫面'),
        ),
        migrations.AddField(
            model_name='articles',
            name='tag',
            field=models.ManyToManyField(blank=True, to='app01.tags', verbose_name='文章標籤'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='avatar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app01.avatars', verbose_name='用戶頭像'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='collects',
            field=models.ManyToManyField(to='app01.articles', verbose_name='收藏的文章'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]