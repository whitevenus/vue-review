from flask import Blueprint, render_template, jsonify

from common.database import model_list
from model.favorite import Favorite

ucenter = Blueprint("ucenter", __name__)


# 在用户中心首页浏览我的收藏，不分页
@ucenter.route('/ucenter')
def user_center():
    result = Favorite().find_my_favorite()
    # print(result)
    list_ = []
    for item in result:
        # print(item._fields)
        dict_item = {}
        cnt = 0
        for row in item:
            # print(row)
            cnt += 1
            dict_ = {}  # 定义字典用于存放一行
            for k, v in row.__dict__.items():  # 遍历列名
                if not k.startswith('_sa_instance_state'):  # 跳过内置字段
                    dict_[k] = v
            if cnt == 1:
                dict_item["favorite"] = dict_
            elif cnt == 2:
                dict_item["article"] = dict_
        list_.append(dict_item)
    # print(list_)
    res_ = {"result": list_}
    return jsonify(res_)
    # return "用户中心页面"
    # return render_template('user-center.html', result=result)


# 切换收藏状态接口
@ucenter.route('/user/favorite/<int:favoriteid>')
def user_favorite(favoriteid):
    canceled = Favorite().switch_favorite(favoriteid)
    return str(canceled)
