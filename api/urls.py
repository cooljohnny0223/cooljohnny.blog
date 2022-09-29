from django.urls import path, re_path
from api.views import login, article, comment

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登入
    path('sign/', login.SignView.as_view()),  # 註冊
    path('article/', article.ArticleView.as_view()),  # 發佈文章
    re_path(r'article/(?P<nid>\d+)/', article.ArticleView.as_view()),  # 編輯文章
    re_path(r'article/comment/(?P<nid>\d+)/', comment.CommentView.as_view()),  # 發佈、刪除評論
    re_path(r'comment/digg/(?P<nid>\d+)/', comment.CommentDiggView.as_view()),  # 評論點讚
    re_path(r'article/digg/(?P<nid>\d+)/', article.ArticleDiggView.as_view()),  # 文章點讚
    re_path(r'article/collects/(?P<nid>\d+)/', article.ArticleCollectsView.as_view()),  # 文章收藏
]
