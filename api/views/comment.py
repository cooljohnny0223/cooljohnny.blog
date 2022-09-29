from django.views import View
from django.http import JsonResponse
from app01.models import Comment, Articles
from django.db.models import F
from api.utils.find_root_sub_comment import find_root_comment
from app01.utils.sub_comment_list import find_root_sub_comment


# 文章評論視圖
class CommentView(View):

    # 發佈評論
    def post(self, request, nid):
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '文章評論成功！！',
            'self': None,
        }
        # 必填資料(文章id、 用戶、評論的內容)
        data = request.data
        if not request.user.username:
            res['msg'] = '請先登入再評論！'
            res['self'] = 'content'
            return JsonResponse(res)

        content = data.get('content')
        if not content:
            res['msg'] = '請輸入評論內容！'
            res['self'] = 'content'
            return JsonResponse(res)
        # 文章評論驗證成功
        # cid 評論id
        cid = data.get('cid')
        # 文章的評論數+1
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)
        if cid:
            # 不是根評論
            comment_obj = Comment.objects.create(
                article_id=nid,
                user=request.user,
                content=content,
                parent_comment_id=cid,
            )
            # 找最終的根評論+1
            root_comment_obj = find_root_comment(comment_obj)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()
        else:
            # 是根評論
            Comment.objects.create(
                article_id=nid,
                user=request.user,
                content=content,
            )
        res['code'] = 0
        return JsonResponse(res)

    # 刪除評論
    def delete(self, request, nid):
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '評論刪除成功！',
        }
        # 自己發佈的評論才能刪除，或者是超級管理員
        # 登入人
        login_user = request.user
        # 評論人
        comment_query = Comment.objects.filter(nid=nid)
        comment_user = comment_query.first().user

        # 獲得傳參的文章編號
        aid = request.data.get('aid')
        # 子評論最終的根評論id
        pid = request.data.get('pid')

        if not (login_user == comment_user or login_user.is_superuser):
            res['msg'] = '用戶驗證失敗'
            return JsonResponse(res)

        # 刪除的是根評論
        # 算子評論數量
        lis = []
        find_root_sub_comment(comment_query.first(), lis)
        Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - len(lis) - 1)

        # 判斷是否為根評論
        if pid:
            # 刪除的是子評論
            # 找最終的根評論 -1
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') - 1)

        comment_query.delete()
        res['code'] = 0
        return JsonResponse(res)


# 評論點讚
class CommentDiggView(View):
    def post(self, request, nid):
        # nid 評論id
        # 返回給前端的資料
        res = {
            'code': 412,
            'msg': '評論點讚成功！！',
            'data': 0,
        }
        # 必須登入才能點讚
        if not request.user.username:
            res['msg'] = '請先登入再點讚！'
            res['self'] = 'content'
            return JsonResponse(res)

        # 評論點讚 +1
        comment_query = Comment.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)

        digg_count = comment_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)
