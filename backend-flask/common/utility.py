import random, string
import time
from email.header import Header
from email.mime.text import MIMEText
from io import BytesIO
from smtplib import SMTP_SSL

from PIL import Image, ImageDraw, ImageFont


# 生成图片验证码
class ImageCode:
    # 生成用于绘制字符串的随机颜色
    @staticmethod
    def rand_color():
        red = random.randint(32, 127)
        green = random.randint(25, 188)
        blue = random.randint(32, 127)
        return red, green, blue

    # 生成4位随机字符串
    @staticmethod
    def gen_text():
        str_ = random.sample(string.ascii_letters + string.digits, 4)
        return ''.join(str_)

    # 划一些干扰线，其中draw为PIL中的ImageDraw对象
    @staticmethod
    def draw_lines(draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width / 2)
            y1 = random.randint(0, height / 2)
            x2 = random.randint(0, width)
            y2 = random.randint(height / 2, height)
            draw.line(((x1, y1), (x2, y2)), fill='black', width=2)

    # 绘制验证码图片
    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50  # 设定图片大小，可根据实际需求调整
        # 创建图片对象，并设定背景色为白色
        im = Image.new('RGB', (width, height), 'white')
        # 选择使用何种字体及字体大小
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)  # 新建ImageDraw对象
        # 绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        # 绘制干扰线
        self.draw_lines(draw, 2, width, height)
        # im.show()   # 如需临时调试，可以直接将生成的图片显示出来
        return im, code

    # 获取图片用于生成图片验证码
    def get_code(self):
        image, code = self.draw_verify_code()
        # 图片以二进制形式写入到内存中而不是硬盘上
        buf = BytesIO()
        image.save(buf, 'jpeg')
        b_string = buf.getvalue()  # 获取图片文件的字节码
        return code, b_string  # 返回验证码的字符串和字节码内容


# 发送QQ邮箱验证码，参数为收件箱地址和随机生成的验证码
def send_email(receiver, ecode):
    sender = 'WoniuNote <2153710263@qq.com>'  # 你的邮箱账号和发件者签名
    # 定义发送邮件的内容，支持HTML标签和CSS样式
    content = f"<br/>欢迎注册蜗牛笔记博客系统账号，您的邮箱验证码为：<span style='color: red; font-size: 20px;'> {ecode} " \
              f"</span>，请复制到注册窗口中完成注册，感谢您的支持。<br/>"
    # 实例化邮件对象，并指定邮件的关键信息
    message = MIMEText(content, 'html', 'utf-8')
    # 指定邮件的标题，同样使用utf-8编码
    message['Subject'] = Header('蜗牛笔记的注册验证码', 'utf-8')
    message['From'] = sender  # 指定发件人信息
    message['To'] = receiver  # 指定收件人邮箱地址

    smtpObj = SMTP_SSL('smtp.qq.com')  # 建议与QQ邮件服务器的连接
    # 通过你的邮箱账号和获取到的授权码登录QQ邮箱
    smtpObj.login(user='2153710263@qq.com', password='flkqyyvdkwtudhgb')
    # 指定发件人，收件人和邮件内容
    smtpObj.sendmail(sender, receiver, str(message))
    smtpObj.quit()  # 发送完成后断开与服务器的连接


# 生成6位随机字符串作为邮箱验证码
def gen_email_code():
    str_ = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str_)


# 压缩图片，通过参数width指定压缩后的图片大小
def compress_image(source, dest, width):
    # 如果图片宽度大于1200，则调整为1200的宽度
    im = Image.open(source)
    x, y = im.size      # 获取源图片的宽和高
    if x > width:
        # 等比例缩放
        ys = int(y * width / x)
        xs = width
        # 调整当前图片的尺寸（同时也会压缩大小）
        temp = im.resize((xs, ys), Image.ANTIALIAS)
        # 将图片保存并使用80%的质量进行压缩
        temp.save(dest, quality=80)
    # 如果尺寸小于指定宽度则不缩减尺寸，只压缩保存
    else:
        im.save(dest, quality=80)


# 解析文章内容中的图片地址
def parse_image_url(content):
    import re
    temp_list = re.findall('<img src="(.+?)"', content)
    url_list = []
    for url in temp_list:
        # 如果图片类型为gif，则直接跳过，不对其作任何处理
        if url.lower().endswith('.gif'):
            continue
        url_list.append(url)
    return url_list


# 远程下载指定URL地址的图片，并保存到临时目录中
def download_image(url, dest):
    import requests
    response = requests.get(url)  # 获取图片的响应
    # 将图片以二进制方式保存到指定文件中
    with open(file=dest, mode='wb') as file:
        file.write(response.content)


# 解析列表中的图片URL地址并生成缩略图，返回缩略图名称
def generate_thumb(url_list):
    # 根据URL地址解析出其文件名和域名
    # 通常建议使用文章内容中的第一张图片来生成缩略图
    # 先遍历url_list，查找里面是否存在本地上传图片，找到即处理，代码运行结束
    for url in url_list:
        if url.startswith('/upload/'):
            filename = url.split('/')[-1]
            # 找到本地图片后对其进行压缩处理，设置缩略图宽度为400像素即可
            compress_image('./static/upload/' + filename,
                           './static/thumb/' + filename, 400)
            return filename

    # 如果在内容中没有找到本地图片，则需要先将网络图片下载到本地再处理
    # 直接将第一张图片作为缩略图，并生成基于时间戳的标准文件名
    url = url_list[0]
    filename = url.split('/')[-1]
    suffix = filename.split('.')[-1]  # 取得文件的后缀名
    thumb_name = time.strftime('%Y%m%d_%H%M%S.' + suffix)
    download_image(url, './static/download/' + thumb_name)
    compress_image('./static/download/' + thumb_name, './static/thumb/' + thumb_name, 400)

    return thumb_name  # 返回当前缩略图的文件名
