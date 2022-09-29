from PIL import Image, ImageDraw, ImageFont  # 引入繪製圖片庫
import string, random  # 引入文字庫、隨機庫
from io import BytesIO  # 引用內存庫

# 全域變數
str_all = string.digits + string.ascii_letters  # 設定數字+英文大小寫字符


# 隨機變化顏色函數
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# 生成驗證碼
def random_code():
    width = 200  # 圖片寬度
    height = 40  # 圖片高度
    white = (255, 255, 255)  # 白色

    # 生成一個的白色背景圖片
    img = Image.new('RGB', (width, height), color=white)

    # 新建一個和圖片同大小的畫布
    draw = ImageDraw.Draw(img)

    # 生成用體對象
    font = ImageFont.truetype(font='./font/Clap Hand.ttf', size=20)

    # 書寫文字
    vaild_code = ''  # 存放驗證碼字串
    for i in range(4):
        random_char = random.choice(str_all)
        draw.text((40 * i + 20, 10), random_char, (0, 0, 0), font=font)
        vaild_code += random_char
    print(vaild_code)

    # 混淆背景設置(點)
    for i in range(100):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), random_color())

    # 混淆背景設置(線)
    for i in range(20):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), random_color())

    # 保存圖片處理
    f = BytesIO()  # 創建一個內存控制代碼
    img.save(f, 'PNG')  # 將圖片保存到內存控制代碼中
    data = f.getvalue() # 讀取內存控制代碼
    print(data)


if __name__ == '__main__':
    random_code()
