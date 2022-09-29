from app01.models import Comment


# 查找根評論的子評論
def find_root_sub_comment(root_comment, sub_comment_list):
    for sub_comment in root_comment.comment_set.all():
        # 找根評論的子評論
        sub_comment_list.append(sub_comment)
        # 遞迴-持續再往下一層級查找子評論
        find_root_sub_comment(sub_comment, sub_comment_list)


def sub_comment_list(nid):
    # 找到某個文章的所有評論
    comment_query = Comment.objects.filter(article_id=nid).order_by('-create_time')
    # 把評論儲存到列表
    comment_list = []

    for comment in comment_query:
        # 如果它的父親是None，就說明是根評論
        if not comment.parent_comment:
            # 遞迴查找這個根評論下面的所有子評論
            lis = []  # 根評論存放子評論的list
            find_root_sub_comment(comment, lis)  # 查找根評論的子評論
            comment.sub_comment = lis  # 將找到的子評論存放在該根評論的list，添加到sub_comment內
            comment_list.append(comment)  # comment_list添加comment資料
            continue

    return comment_list
