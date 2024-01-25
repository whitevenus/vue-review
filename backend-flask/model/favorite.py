from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time

from model.article import Article

dbsession, md, DBase = dbconnect()


class Favorite(DBase):
    __table__ = Table("favorite", md, autoload=True)

    # 插入文章收藏数据
    @staticmethod
    def insert_favorite(article_id):
        # 如果是之前已经收藏后来取消收藏的文章，则直接修改其状态
        row = dbsession.query(Favorite).filter_by(articleid=article_id, userid=session.get('userid')).first()
        if row is not None:
            row.canceled = 0
        else:
            now = time.strftime('%Y-%m-%d %H:%M:%S')
            favorite = Favorite(articleid=article_id, userid=session.get('userid'),
                                canceled=0, createtime=now, updatetime=now)
            dbsession.add(favorite)
        dbsession.commit()

    # 取消文章收藏
    @staticmethod
    def cancel_favorite(article_id):
        row = dbsession.query(Favorite).filter_by(articleid=article_id, userid=session.get('userid')).first()
        row.canceled = 1
        dbsession.commit()

    # 判断文章是否已经被收藏
    @staticmethod
    def check_favorite(article_id):
        row = dbsession.query(Favorite).filter_by(articleid=article_id, userid=session.get('userid')).first()
        if row is None:
            return False
        elif row.canceled == 1:
            return False
        else:
            return True

    # 为用户中心查询我的收藏添加数据操作方法
    @staticmethod
    def find_my_favorite():
        print(session.get('userid'))
        result = dbsession.query(Favorite, Article).join(Article, Favorite.articleid ==
                                                         Article.articleid).filter(
            Favorite.userid == session.get('userid')).all()
        return result

    # 切换收藏和取消收藏的状态
    @staticmethod
    def switch_favorite(favoriteid):
        row = dbsession.query(Favorite).filter_by(favoriteid=favoriteid).first()
        if row.canceled == 1:
            row.canceled = 0
        else:
            row.canceled = 1
        dbsession.commit()
        return row.canceled
