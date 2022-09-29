from urllib.parse import urlencode


# 搜尋
class Search:
    def __init__(self, key, order, order_list, query_params):
        self.key = key
        self.order_list = order_list
        self.order = order
        self.query_params = {}
        for i in query_params:
            self.query_params[i] = query_params.getlist(i)

    def order_html(self):
        order_list = []
        check_order = ''  # 檢查參數是否在列表中
        for li in self.order_list:
            self.query_params[self.key] = li[0]
            if self.order == li[0]:
                li = f'<li class="active"><a href="?{self.query_encode}">{li[1]}</a></li>'
                check_order = '檢查通過'
            else:
                li = f'<li><a href="?{self.query_encode}">{li[1]}</a></li>'
            order_list.append(li)

        # 默認選中(沒有參數或防止隨便修改傳參)
        if not self.key or check_order == '':
            # 沒有傳遞order
            str_li = order_list[0]
            # 切片拼接 active 選中狀態
            new_str = str_li[0:3] + ' class="active"' + str_li[3:]
            order_list[0] = new_str
        return ''.join(order_list)

    @property
    def query_encode(self):
        return urlencode(self.query_params, doseq=True)