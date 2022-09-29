# 配置 Django環境
import os

if __name__ == '__main__':
    # 加載Django項目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v4_blog.settings")
    # 導入Django，並啟動Django項目
    import django

    django.setup()

    from app01.models import Articles, Comment

    # 方案一(使用字典的方式)：
    # 思想：根據子評論遞回查找根評論
    """
    {
    父評論1_nid：{
    
        所有子評論:[
        {},{},{}
        ]
    },
    父評論2_nid：{
    
    },
    }
    
    """

    # 找到這個子評論的最終根評論，返回根評論對象
    def find_root_comment(comment: Comment):
        if comment.parent_comment:
            # 還不是根評論
            # 遞回去找它的根評論
            return find_root_comment(comment.parent_comment)
        # 是根評論，就返回出去
        return comment

    # 評論字典
    comment_dict = {
    }

    # 找到某個文章的所有評論
    comment_query = Comment.objects.filter(article_id=5)

    for comment in comment_query:
        # 如果它的父親是None，就說明是根評論
        if not comment.parent_comment:
            # 把根評論放入字典
            comment_dict[comment.nid] = comment
            # 給根評論添加自定義屬性，將所有的子評論放進去
            comment.sub_comment = []
            continue

    for comment in comment_query:
        # 一定是某個父評論的子評論
        for sub_comment in comment.comment_set.all():
            # 循環該評論下面的所有子評論
            # find_root_comment:找到這個子評論的最終根評論，返回根評論對象
            root_comment = find_root_comment(sub_comment)
            # 把子評論添加到屬於自己的根評論裡面
            comment_dict[root_comment.nid].sub_comment.append(sub_comment)

    for k, v in comment_dict.items():
        print(v, '根評論')
        for comment in v.sub_comment:
            print('  ', comment, '子評論')
