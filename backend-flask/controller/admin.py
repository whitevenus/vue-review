import math

from flask import Blueprint, jsonify, session

# 添加控制器admin并实现入口：
from common.database import model_list_single
from model.article import Article

admin = Blueprint("admin", __name__)


@admin.route('/admin')
def sys_admin():
    pagesize = 15
    result = Article.find_all_except_draft(0, pagesize)
    total = math.ceil(Article.get_count_except_draft() / pagesize)
    # print(result)
    res = model_list_single(result)
    # print(res[0])
    # print(total)
    dict_ = {"page": 1, "result": res, "total": total}
    return jsonify(dict_)
    # return render_template('system-admin.html', page=1, result=result, total=total)


# 为系统管理首页的文章列表进行分页查询
@admin.route('/admin/article/<int:page>')
def admin_article(page):
    # print(page)
    pagesize = 15
    start = (page - 1) * pagesize
    result = Article.find_all_except_draft(start, pagesize)
    total = math.ceil(Article.get_count_except_draft() / pagesize)
    res = model_list_single(result)
    dict_ = {"page": page, "result": res, "total": total}
    return jsonify(dict_)
    # return "文章管理分页查询接口"
    # return render_template('system-admin.html', page=page, result=result, total=total)


# 按照文章进行分类搜索的后台接口
@admin.route('/admin/type/<int:type>-<int:page>')
def admin_search_type(type, page):
    pagesize = 15
    start = (page - 1) * pagesize
    result, total = Article().find_by_type_except_draft(start, pagesize, type)
    total = math.ceil(total / pagesize)
    # print(result)
    # print(total)
    res = model_list_single(result)
    dict_ = {"page": page, "result": res, "total": total}
    return jsonify(dict_)

    # return render_template('system-admin.html', page=page, result=result, total=total)


# 按照文章标题进行模糊查询的后台接口
@admin.route('/admin/search/<keyword>')
def admin_search_headline(keyword):
    result = Article().find_by_headline_except_draft(keyword)
    res = model_list_single(result)
    dict_ = {"page": 1, "result": res, "total": 1}
    return jsonify(dict_)
    # return render_template('system-admin.html', page=1, result=result, total=1)


# 文章的隐藏切换接口
@admin.route('/admin/article/hide/<int:articleid>')
def admin_article_hide(articleid):
    hidden = Article().switch_hidden(articleid)
    return str(hidden)


# 文章的推荐切换接口
@admin.route('/admin/article/recommend/<int:articleid>')
def admin_article_recommend(articleid):
    recommended = Article().switch_recommended(articleid)
    return str(recommended)


# 文章的审核切换接口
@admin.route('/admin/article/check/<int:articleid>')
def admin_article_check(articleid):
    checked = Article().switch_checked(articleid)
    return str(checked)
