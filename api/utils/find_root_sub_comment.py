# 找到這個子評論的最終根評論，返回根評論對象
def find_root_comment(comment):
    if comment.parent_comment:
        # 還不是根評論
        # 遞回去找它的根評論
        return find_root_comment(comment.parent_comment)
    # 是根評論，就返回出去
    return comment