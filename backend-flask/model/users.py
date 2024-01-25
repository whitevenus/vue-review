import random
import time

from flask import session
from sqlalchemy import Table
from common.database import dbconnect

dbsession, md, DBase = dbconnect()  # 获取构建SQLAlchemy的3个必须对象


# 定义users表的关系模型
class Users(DBase):
    __table__ = Table("users", md, autoload=True)

    @staticmethod
    def find_all():
        result = dbsession.query(Users).all()
        return result

    # 查询用户名，可用于注册时判断用户名是否已注册，也可用于登录校验
    @staticmethod
    def find_by_username(username):
        result = dbsession.query(Users).filter_by(username=username).all()
        return result

    # 查询用户名，可用于注册时判断用户名是否已注册，也可用于登录校验
    @staticmethod
    def find_by_userid(userid):
        result = dbsession.query(Users).filter_by(userid=userid).first()
        # print(result)
        return result

    # 实现注册，首次注册时用户只需要输入用户名和密码，所以只需要两个参数
    # 注册时，在模型类中为其他字段尽力生成一些可用的值，虽不全面，但可用
    # 通常用户注册时不建议填写太多资料，影响体验，可待用户后续逐步完善
    @staticmethod
    def do_register(username, password):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        nickname = username.split('@')[0]  # 默认将邮箱账号前缀作为昵称
        avatar = str(random.randint(1, 15))  # 从15张头像图片中随机选择一张
        user = Users(username=username, password=password, role='user', nickname=nickname, credit=50,
                     avatar=avatar + '.png', createtime=now, updatetime=now)
        dbsession.add(user)
        dbsession.commit()
        return user

    # 修改用户剩余积分，积分为正数表示增加积分，为负数表示减少积分
    @staticmethod
    def update_credit(credit):
        user = dbsession.query(Users).filter_by(userid=session.get('userid')).one()
        user.credit += credit
        dbsession.commit()
