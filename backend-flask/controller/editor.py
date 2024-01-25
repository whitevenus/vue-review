import time

from flask import Blueprint, render_template, session, request, jsonify

from common.utility import compress_image

editor = Blueprint("editor", __name__)


@editor.route('/edit', methods=['GET', 'POST'])
def edit():
    # 根据UEditor的接口定义规则，如果前端参数为action=config，
    # 则表示试图请求后台的config.json文件，请求成功则说明后台接口能正常工作
    param = request.args.get('action')
    if request.method == 'GET' and param == 'config':
        return render_template('config.json')
        # return "hello"

    # 构造上传图片的接口，并对图片进行压缩处理
    elif request.method == 'POST' and request.args.get('action') == 'upload_image':
        f = request.files['up_file']  # 获取前端图片文件数据
        filename = f.filename
        # 为上传来的文件生成统一的文件名
        suffix = filename.split('.')[-1]  # 取得文件的后缀名
        newname = time.strftime('%Y%m%d_%H%M%S.' + suffix)
        f.save('./resource/upload/' + newname)  # 保存图片

        # 对图片进行压缩，按照1200像素宽度为准，并覆盖原始文件
        source = dest = './resource/upload/' + newname
        compress_image(source, dest, 1200)

        result = {'state': 'SUCCESS', "url": f"http://127.0.0.1:5000/upload/{newname}", 'title': filename,
                  'original': filename}  # 构造响应数据
        # 系统上线到公网后，域名一定不是127.0.0.1，端口也不再是5000，需要同步修改

        return jsonify(result)  # 以JSON数据格式返回响应，供前端编辑器引用
