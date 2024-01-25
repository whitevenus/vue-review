import math

from flask import Blueprint, jsonify
from model.article import Article
from common.database import model_list


index = Blueprint("index", __name__)


@index.route('/get_index_article')
def home():    # 注意该函数名不能与blueprint模块名相同
    article = Article()
    result = article.find_limit_with_users(0, 10)    # 首页只显示10条，暂不分页
    res = model_list(result)
    total = math.ceil(article.get_total_count() / 10)
    dict_ = {"total": total, "page": 1, "result": res}
    return jsonify(dict_)
    # return render_template('index.html', result=result)


@index.route('/page/<int:page>')
def paginate(page):
    pagesize = 10
    start = (page - 1) * pagesize  # 根据当前页码定义数据的起始位置

    article = Article()
    result = article.find_limit_with_users(start, pagesize)

    total = math.ceil((article.get_total_count() / 10))  # 根据数据总量计算总页数

    res_json = model_list(result)
    # print(res_json)
    # print(total)
    # print(page)
    # 将相关数据传递给模板页面，从模板引擎调用
    # return render_template('index.html', result=result, page=page, total=total)
    dict_ = {"total": total, "page": page, "result": res_json}
    return jsonify(dict_)
