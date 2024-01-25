import hashlib
import re

from flask import Blueprint, make_response, session, request, jsonify, redirect, url_for

from common.utility import ImageCode, gen_email_code, send_email
from model.credit import Credit
from model.users import Users

user = Blueprint("user", __name__)


@user.route('/vcode')
def vcode():
    code, b_string = ImageCode().get_code()
    response = make_response(b_string)  # 将响应的内容设置为验证码
    response.headers['Content-Type'] = 'image/jpeg'
    session['vcode'] = code.lower()  # 转换成小写字母保存到Session变量中
    return response


@user.route('/ecode', methods=['POST'])
def ecode():
    email = request.form.get('email')
    # 导入Python的正则表达式re模板，后台同步验证邮箱地址正确性
    if not re.match('.+@.+\..+', email):
        return 'email-invalid'
    code = gen_email_code()
    try:
        send_email(email, code)
        session['ecode'] = code.lower()
        return 'send-pass'
    except:
        return 'send-fail'


# 无论注册成功还是失败，都响应给前端一个字符串值用于标识注册状态
@user.route('/user', methods=['POST'])
def register():
    user_ = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    ecode_ = request.form.get('ecode').lower().strip()

    if ecode_ != session.get('ecode'):
        dict_ = {"info": "ecode-error", "session": session}
        return jsonify(dict_)
        # return 'ecode-error'
    # 注册时继续验证邮箱地址的正确性
    elif not re.match('.+@.+\..+', username) or len(password) < 5:
        dict_ = {"info": "up-invalid", "session": session}
        return jsonify(dict_)
        # return 'up-invalid'
    elif len(user_.find_by_username(username)) > 0:
        dict_ = {"info": "user-repeated", "session": session}
        return jsonify(dict_)
        # return 'user-repeated'
    else:
        # 将密码转换为MD5进行保存
        password = hashlib.md5(password.encode()).hexdigest()
        result = user_.do_register(username, password)
        try:
            # 注册成功后，保存以下三个变量到Session中供后续代码使用
            session['isLogin'] = 'true'
            session['userid'] = result.userid
            session['username'] = username
            session['nickname'] = result.nickname
            session['role'] = result.role
            # 同时，为credit表添加一条积分明细
            Credit().insert_detail(type_='用户注册', target='0', credit=50)
            dict_ = {"info": "reg-pass", "session": session}
            return jsonify(dict_)
            # return 'reg-pass'
        except:
            dict_ = {"info": "reg-fail", "session": session}
            return jsonify(dict_)
            # return 'reg-fail'


@user.route('/login', methods=['POST'])
def login():
    user_ = Users()
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    vcode_ = request.form.get('vcode').lower().strip()
    # print(session)
    if vcode_ != session.get('vcode'):
        dict_ = {"info": "vcode-error", "session": session}
        return jsonify(dict_)
        # return 'vcode-error'
    else:
        # 将密码转换为MD5进行验证
        password = hashlib.md5(password.encode()).hexdigest()
        result = user_.find_by_username(username)
        # 如果根据用户名找到唯一数据且密码可以与之匹配，则登录成功
        if len(result) == 1 and result[0].password == password:
            session['isLogin'] = 'true'
            session['userid'] = result[0].userid
            session['username'] = username
            session['nickname'] = result[0].nickname
            session['role'] = result[0].role
            # 为积分表增加1分的登录明细，同时修改用户表的总积分
            Credit().insert_detail(type_='正常登录', target='0', credit=1)
            user_.update_credit(1)

            dict_ = {"info": "login-pass", "session": session}
            return jsonify(dict_)
            # return 'login-pass'
        else:
            dict_ = {"info": "login-fail", "session": session}
            return jsonify(dict_)
            # return 'login-fail'


@user.route('/logout')
def logout():
    session.clear()     # 清空所有Session变量
    return jsonify({"session": session})
    # return redirect(url_for('index.home'))   # 跳转到首页

