from flask import session
from sqlalchemy import Table
from common.database import dbconnect
import time

dbsession, md, DBase = dbconnect()


class Credit(DBase):
    __table__ = Table("credit", md, autoload=True)

    @staticmethod
    def insert_detail(type_, target, credit):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        # print("更新Credit")
        # print(session.get("userid"))
        credit = Credit(userid=session.get('userid'), category=type_, target=target,
                        credit=credit, createtime=now, updatetime=now)
        dbsession.add(credit)
        dbsession.commit()

    # 判断用户是否已经消耗了积分
    @staticmethod
    def check_payed_article(article_id):
        result = dbsession.query(Credit).filter_by(userid=session.get('userid'),
                                                   target=article_id).all()
        if len(result) > 0:
            return True  # 表示已经消耗了积分，勿需继续消耗
        else:
            return False
