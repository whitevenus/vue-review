from flask import Blueprint, abort, jsonify, request, session

from common.database import model_list
from common.utility import parse_image_url, generate_thumb
from model.article import Article
from model.comment import Comment
from model.credit import Credit
from model.favorite import Favorite
from model.users import Users

article = Blueprint("article", __name__)


@article.route('/article/<int:article_id>')
def read(article_id):
    # dict_ = {"result": ""}
    result = ""
    try:
        result = Article().find_by_id(article_id)
        if result is None:
            abort(404)  # 如果文章编号不正确，则直接到404页面
    except:
        abort(500)  # 出现异常则直接到500页面

    article_ = result[0]
    # 由于直接修改article.content的值会导致数据表内容的修改
    # 所以将result中的值取出来保存到字典中，不直接操作result中的article对象
    dict_ = {}
    for k, v in article_.__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict_[k] = v
    dict_['nickname'] = result.nickname

    # 如果用户已经消耗了积分，则不再截取文章内容
    payed = Credit().check_payed_article(article_id)

    position = 0
    if not payed:
        if dict_['credit'] > 0:  # 表示是积分阅读的文章
            content = dict_['content']  # 获取文章内容
            temp = content[0:int(len(content) / 2)]  # 截取前面一半的内容
            position = temp.rindex('</p>') + 4  # 在截取内容中查找最后一个</p>位置
            dict_['content'] = temp[0:position]

    Article().update_read_count(article_id)  # 增加1次阅读次数

    # 获取文章是否已经被收藏的标识
    is_favorite = Favorite().check_favorite(article_id)

    # 获取当前文章的上一篇和下一篇
    prev_next = Article().find_prev_next_by_id(article_id)

    # 显示文章对应的评论
    comment_user = Comment().find_limit_with_user(article_id, 0, 50)
    # print(comment_user)
    com_user = model_list(comment_user)
    # print(com_user)
    res = {"article": dict_, "position": position, "payed": payed, "is_favorite": is_favorite, "prev_next": prev_next,
           "comment_user": com_user}
    # print(dict_)
    return jsonify(res)

    # return render_template('article-user.html', result=result)


# 为article控制器添加read_all接口
@article.route('/readall', methods=['POST'])
def read_all():
    # print(request.form.get("position"))
    position = int(request.form.get('position'))
    article_id = request.form.get('article_id')
    article_ = Article()
    result = article_.find_by_id(article_id)
    content = result[0].content[position:]  # 读取剩余内容

    # 添加是否已经消耗积分的判断
    payed = Credit().check_payed_article(article_id)
    if not payed:
        # 为积分表添加阅读文章的消耗明细
        Credit().insert_detail(type_='阅读文章', target=article_id, credit=-1 * result[0].credit)
        # 同步更新用户表，剩余积分减去当前消耗的积分
        Users().update_credit(credit=-1 * result[0].credit)

    return content


@article.route('/article', methods=['POST'])
def add_article():
    headline = request.form.get('headline')
    content = request.form.get('content')
    type_ = int(request.form.get('type'))
    credit = int(request.form.get('credit'))
    drafted = int(request.form.get('drafted'))
    checked = int(request.form.get('checked'))
    article_id = int(request.form.get("article_id"))

    print(session)
    if session.get('userid') is None:
        return 'perm-denied'
    else:
        user = Users().find_by_userid(session.get('userid'))
        print(user)
        if user.role == 'editor':
            # 权限合格，可以执行发布文章的代码
            # 首先为文章生成缩略图，优先从内容中找，找不到则随机生成一张
            url_list = parse_image_url(content)
            if len(url_list) > 0:  # 表示文章中存在图片
                thumb_name = generate_thumb(url_list)
            else:
                # 如果文章中没有图片，则根据文章类别指定一张缩略图
                thumb_name = '%d.png' % type_

            if article_id == 0:
                try:
                    id_ = Article().insert_article(type_=type_, headline=headline, content=content, credit=credit,
                                                   thumbnail=thumb_name, drafted=drafted, checked=checked)
                    return str(id_)
                except Exception as e:
                    return 'post-fail'
            else:
                # 如果是已经添加过的文章，则做修改操作
                try:
                    id_ = Article.update_article(article_id=article_id, type_=type_,
                                                 headline=headline, content=content, credit=credit,
                                                 thumbnail=thumb_name, drafted=drafted, checked=checked)
                    return str(id_)
                except:
                    return 'post-fail'
        # 如果角色不是作者，则只能投稿，不能正式发布
        elif checked == 1:
            return 'perm-denied'
        else:
            return 'perm-denied'
