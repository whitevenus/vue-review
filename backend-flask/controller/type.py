from flask import Blueprint, jsonify
from model.article import Article
import math
from common.database import model_list

type_ = Blueprint("type", __name__)


@type_.route('/type/<string>')
def classify(string):
    # print(string)
    # 前端传过来的string的格式为 1-1, 2-3，所以需要使用split拆分为type和page
    _type = int(string.split('-')[0])
    page = int(string.split('-')[1])

    pagesize = 10
    start = (page - 1) * pagesize   # 根据当前页码定义数据的起始位置

    article = Article()
    result = article.find_by_type(_type, start, pagesize)
    # print(result)
    res = model_list(result)
    total = math.ceil(article.get_count_by_type(_type) / pagesize)     # 计算总页数
    # print(total)
    dict_ = {"total": total, "page": page, "result": res, "type": _type}
    return jsonify(dict_)
    # 由于分类页面与首页文章列表功能一致，所以直接使用index.html作为模板页面
    # return render_template('index.html', result=result, page=page, total=total)
