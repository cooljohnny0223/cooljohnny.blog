# 測試
import os

if __name__ == '__main__':
    # 加載Django項目的配置信息
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v4_blog.settings")
    # 導入Django，並啟動Django項目
    import django

    django.setup()

    from app01.models import Moods
    # from api.utils.get_user_info import get_addr_info

    mood_query = Moods.objects.all()
    for obj in mood_query:
        print(obj.addr, type(obj.addr))
        # 將資料寫入到資料庫
        # addr = get_addr_info(obj.ip)
        # obj.addr = addr
        # obj.save()
