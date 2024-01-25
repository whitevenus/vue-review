from flask import Blueprint, request
from model.comment import Comment
from model.credit import Credit
from model.users import Users
from model.article import Article

comment = Blueprint("comment", __name__)


# 遵循REST ful风格的接口，用于新增评论
@comment.route('/comment', methods=['POST'])
def add():
    article_id = request.form.get('article_id')
    content = request.form.get('content')
    ipaddr = request.remote_addr

    print(ipaddr)

    # 如果评论的字数低于5个或多于1000个，均视为不合法
    if len(content) < 5 or len(content) > 1000:
        return 'content-invalid'

    comment_ = Comment()
    # 没有超出限制才能发表评论
    if not comment_.check_limit_per_5():
        try:
            comment_.insert_comment(article_id=article_id, content=content, ipaddr=ipaddr)

            # print("插入评论成功")

            # 评论成功后，同步更新credit表明细、users表积分和article表回复数
            Credit().insert_detail(type_='添加评论', target=article_id, credit=2)

            Users().update_credit(2)
            # print("更新用户积分成功")
            Article().update_reply_count(article_id)
            return 'add-pass'
        except:
            return 'add-fail'
    else:
        return 'add-limit'
