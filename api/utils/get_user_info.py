import re
import requests

# 簡轉繁套件
from opencc import OpenCC

# 反爬
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}


# 獲取IP位址
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判斷是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理獲取真實IP
        return ip
    ip = request.META.get('REMOTE_ADDR')  # 未使用代理獲散IP
    return ip


# 獲取用戶位址
def get_addr_info(ip):
    # 判斷內部網段
    if ip.startswith('10.') or ip.startswith('192') or ip.startswith('127'):
        return {"city": "內網", "prov": "臺灣省"}
    url = f'https://www.ip138.com/iplookup.asp?ip={ip}&action=2'
    # 獲取字節碼
    res = requests.get(url=url, headers=headers).content.decode('gbk')
    # 簡轉繁
    cc = OpenCC('s2tw')
    twStr = cc.convert(res)
    # 只取得要的資料
    result = re.findall(r'ip_result = (.*?);', twStr, re.S)[0]

    # 使用eval變成字典
    consequence = eval(result)
    addr = consequence['ip_c_list'][0]
    # 刪除不要的欄位
    addr.pop('begin')
    addr.pop('end')
    addr.pop('idc')
    addr.pop('net')
    area = addr.get('area')
    if not area:
        addr.pop('area')
    return addr


if __name__ == '__main__':
    get_addr_info('114.33.106.143')
