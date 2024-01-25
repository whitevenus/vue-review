from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time

from model.users import Users

dbsession, md, DBase = dbconnect()


class Comment(DBase):
    __table__ = Table("comment", md, autoload=True)

    # 新增一条评论
    @staticmethod
    def insert_comment(article_id, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(userid=session.get('userid'), articleid=article_id,
                          content=content, ipaddr=ipaddr, createtime=now, updatetime=now)
        dbsession.add(comment)
        dbsession.commit()

    # 根据文章编号查询所有评论
    @staticmethod
    def find_by_article_id(article_id):
        result = dbsession.query(Comment).filter_by(articleid=article_id, hidden=0).all()
        return result

    # 根据用户编号和日期进行查询是否已经超过每天5条限制
    @staticmethod
    def check_limit_per_5():
        start = time.strftime("%Y-%m-%d 00:00:00")  # 当天的起始时间
        end = time.strftime("%Y-%m-%d 23:59:59")  # 当天的结束时间
        result = dbsession.query(Comment).filter(Comment.userid ==
                                                 session.get('userid'), Comment.createtime.between(start, end)).all()
        if len(result) >= 5:
            return True  # 返回True表示今天已经不能再发表评论
        else:
            return False

    # 查询评论与用户信息，注意评论也需要分页
    @staticmethod
    def find_limit_with_user(article_id, start, count):
        result = dbsession.query(Comment, Users).join(Users, Users.userid ==
                                                      Comment.userid).filter(Comment.articleid == article_id,
                                                                             Comment.hidden == 0) \
            .order_by(Comment.commentid.desc()).limit(count).offset(start).all()
        return result
