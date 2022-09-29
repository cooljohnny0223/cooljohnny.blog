import math
from urllib.parse import urlencode


# 網址後面傳遞參數的格式
# query_params = {'tag': 'python', 'page': '1'}
# print(urlencode(query_params))
# 印出效果：tag=python&page=1


class Pagination:
    def __init__(self, current_page, all_count, base_url, query_params, per_page=20, pager_page_count=11):
        """
        :param current_page: 當前頁碼
        :param all_count: 資料庫中的總筆數
        :param base_url: 原始url
        :param query_params: 保留原搜尋條件
        :param per_page: 一頁展示多少條
        :param pager_page_count: 最多顯示多少個頁碼  數值為奇數較佳分配 例數值11： 5 1 5
        """

        self.all_count = all_count
        self.per_page = per_page

        # 計算一共有多少個頁碼
        # (劣)1、取餘數 divmod()
        #    100/ 9 = 11 餘 1
        #    100 /10 = 10 餘 0
        # div, p = divmod(all_count, per_page)
        # if p != 0:
        #     div += 1
        # self.current_count = div

        # (優)2、進位 math.cell(11.000001)  --> 12

        # 可以分的頁數
        self.current_count = math.ceil(all_count / per_page)

        # 只能是滿足條件的數字
        try:
            self.current_page = current_page
            # 校驗 如果當前頁碼 小於0 和小於等於總頁碼數 不成立，當前頁碼還是等於1
            if not 0 < self.current_page <= self.current_count:
                self.current_page = 1
        except Exception:
            self.current_page = 1

        self.base_url = base_url
        self.query_params = query_params
        self.pager_page_count = pager_page_count

        # 分頁的中間值
        self.half_paper_count = int(self.pager_page_count / 2)
        # 如果可分頁的頁碼小於最大顯示頁碼，就讓最大顯示頁碼變成可分頁頁碼
        if self.current_count < self.pager_page_count:
            self.pager_page_count = self.current_count

        # print(self.current_page, self.current_count)

    # 生成頁碼-最大頁碼長度處理
    def page_html(self):
        # 計算頁碼的起始和結束
        # 分類討論
        # 1、正常情況
        # 20 9    4 5 6 7 8 9 10 11 12 13 14
        start = self.current_page - self.half_paper_count
        end = self.current_page + self.half_paper_count
        # 2、特殊情況
        # 在最左側
        if self.current_page <= self.half_paper_count:
            start = 1
            # 右邊就是最大值
            end = self.pager_page_count
        # 在最右側
        if self.current_page + self.half_paper_count >= self.current_count:
            start = self.current_count - self.pager_page_count
            end = self.current_count
        # 生成分頁
        page_list = []

        # 上一頁
        if self.current_page != 1:
            self.query_params['page'] = self.current_page - 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">上一頁</a></li>')

        # 數字部份
        for i in range(start, end + 1):
            self.query_params['page'] = i
            if self.current_page == i:
                # 選中的分頁頁碼
                li = f'<li class="active"><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            else:
                li = f'<li><a href="{self.base_url}?{self.query_encode}">{i}</a></li>'
            page_list.append(li)

        # 下一頁
        if self.current_page != self.current_count:
            self.query_params['page'] = self.current_page + 1
            page_list.append(f'<li><a href="{self.base_url}?{self.query_encode}">下一頁</a></li>')

        return ''.join(page_list)

    # 測試用
    @property
    def query_encode(self):
        return urlencode(self.query_params)

    # 開始位置----方法加上@property，以後呼叫這個方法就不用加()
    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    # 結束位置----方法加上@property，以後呼叫這個方法就不用加()
    @property
    def end(self):
        return self.current_page * self.per_page


if __name__ == '__main__':
    # 計算分頁切片區間
    # 1 2 3 4 5 6 7 8 9 10
    # 1 0 2    [((頁碼-1)*每頁展示的條數):(頁碼*每頁展示的條數)]
    # 2 2 4
    # 5 8 10
    pager = Pagination(
        current_page=1,
        all_count=100,
        base_url='/article',
        query_params={'tag': 'python', 'name': '尚豪'},
        per_page=5,
        pager_page_count=7,
    )
    # print(page.start, page.end)
    print(pager.page_html())
