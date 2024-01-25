import time

from flask import session
from sqlalchemy import Table
from common.database import dbconnect
from model.users import Users

dbsession, md, DBase = dbconnect()  # 获取构建SQLAlchemy的3个必须对象


# 定义article表的关系模型
class Article(DBase):
    __table__ = Table("article", md, autoload=True)

    # 获取文章总数
    @staticmethod
    def get_total_count():
        count = dbsession.query(Article.articleid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1).count()
        return count

    # 查询article表中所有数据并返回结果集
    @staticmethod
    def find_all():
        result = dbsession.query(Article).order_by(Article.articleid.desc()).all()
        return result

    #
    # # 根据id查询article表中唯一数据，并返回该行记录
    # @staticmethod
    # def find_by_id(article_id):
    #     row = dbsession.query(Article).filter_by(article_id=article_id).first()
    #     return row

    # 与users表进行连接查询并获取用户信息，同时只返回10条数据
    # 设计本方法的目的在于，首页不可能一次性将所有文章全部显示，必然要做分页
    @staticmethod
    def find_limit_with_users(start, count):
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 根据文章类别查询文章，并进行分页查询
    @staticmethod
    def find_by_type(type_, start, count):
        result = dbsession.query(Article, Users).join(Users, Users.userid == Article.userid) \
            .filter(Article.hidden == 0, Article.drafted == 0, Article.checked == 1, Article.type == type_) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 根据文章类型获取文章数量
    @staticmethod
    def get_count_by_type(type_):
        count = dbsession.query(Article.articleid).filter(Article.hidden == 0,
                                                          Article.drafted == 0, Article.checked == 1,
                                                          Article.type == type_).count()
        return count

    # 根据id查询article表中唯一数据，并返回该行记录
    @staticmethod
    def find_by_id(article_id):
        row = dbsession.query(Article, Users.nickname).join(Users, Users.userid == Article.userid).filter(
            Article.hidden == 0, Article.drafted == 0, Article.checked == 1,
            Article.articleid == article_id).first()
        # 结果集格式：(<model.article.Article object at 0x11B39770>, '强哥')，注意取值
        return row

    # 每阅读一次文章，阅读次数+1
    @staticmethod
    def update_read_count(article_id):
        article = dbsession.query(Article).filter_by(articleid=article_id).one()
        article.readcount += 1
        dbsession.commit()

    # 根据文章编号查询文章标题
    @staticmethod
    def find_headline_by_id(article_id):
        row = dbsession.query(Article.headline).filter_by(
            articleid=article_id).first()
        return row.headline

    # 查询当前文章的上一篇和下一篇的文章编号和标题
    def find_prev_next_by_id(self, article_id):
        dict_ = {}  # 用字典保存相关信息并返回

        # 查询比当前编号小的编号中最大的一个，即上一篇
        row = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0,
                                              Article.checked == 1, Article.articleid < article_id). \
            order_by(Article.articleid.desc()).limit(1).first()
        # 如果没有查询到比当前编号更小的，说明是第一篇，则上一篇依然是当前文章
        if row is None:
            prev_id = article_id
        else:
            prev_id = row.articleid

        dict_['prev_id'] = prev_id
        dict_['prev_headline'] = self.find_headline_by_id(prev_id)

        # 查询比当前编号大的编号中最小的一个，即下一篇
        row = dbsession.query(Article).filter(Article.hidden == 0, Article.drafted == 0,
                                              Article.checked == 1, Article.articleid > article_id). \
            order_by(Article.articleid).limit(1).first()
        # 如果没有查询到比当前编号更大的，说明是最后一篇，则下一篇依然是当前文章
        if row is None:
            next_id = article_id
        else:
            next_id = row.articleid

        dict_['next_id'] = next_id
        dict_['next_headline'] = self.find_headline_by_id(next_id)

        return dict_

    # 当发表或者回复评论后，为文章表字段reply_count加1
    @staticmethod
    def update_reply_count(article_id):
        row = dbsession.query(Article).filter_by(articleid=article_id).first()
        row.replycount += 1
        dbsession.commit()

    # 插入一篇新的文章，草稿或投稿通过参数进行区分
    @staticmethod
    def insert_article(type_, headline, content, thumbnail, credit, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        userid = session.get('userid')
        # 其他字段在数据库中均已设置好默认值，无须手工插入
        article = Article(userid=userid, type=type_, headline=headline, content=content,
                          thumbnail=thumbnail, credit=credit, drafted=drafted,
                          checked=checked, createtime=now, updatetime=now)
        dbsession.add(article)
        dbsession.commit()

        return article.articleid  # 将新的文章编号返回，便于前端页面跳转

    # 根据文章编号更新文章的内容，可用于文章编辑或草稿修改，以及基于草稿的发布
    @staticmethod
    def update_article(article_id, type_, headline, content, thumbnail, credit, drafted=0, checked=1):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        row = dbsession.query(Article).filter_by(articleid=article_id).first()
        row.type = type_
        row.headline = headline
        row.content = content
        row.thumbnail = thumbnail
        row.credit = credit
        row.drafted = drafted
        row.checked = checked
        row.updatetime = now  # 修改文章的更新时间
        dbsession.commit()
        return article_id  # 继续将文章ID返回调用处

    # 查询article表中除草稿外的所有数据并返回结果集
    @staticmethod
    def find_all_except_draft(start, count):
        result = dbsession.query(Article).filter(Article.drafted == 0) \
            .order_by(Article.articleid.desc()).limit(count).offset(start).all()
        return result

    # 查询除草稿外的所有文章的总数量
    @staticmethod
    def get_count_except_draft():
        count = dbsession.query(Article).filter(Article.drafted == 0).count()
        return count

    # 按照文章分类进行查询（不含草稿，该方法直接返回文章总数量用于分页）
    def find_by_type_except_draft(self, start, count, type):
        if type == 0:
            result = self.find_all_except_draft(start, count)
            total = self.get_count_except_draft()
        else:
            result = dbsession.query(Article).filter(Article.drafted == 0,
                                                     Article.type == type).order_by(Article.articleid.desc()) \
                .limit(count).offset(start).all()
            total = dbsession.query(Article).filter(Article.drafted == 0,
                                                    Article.type == type).count()
        return result, total  # 返回分页结果集和不分页的总数量

    # 按照标题模糊查询（不含草稿，不分页）
    @staticmethod
    def find_by_headline_except_draft(headline):
        result = dbsession.query(Article).filter(Article.drafted == 0,
                                                 Article.headline.like('%' + headline + '%')) \
            .order_by(Article.articleid.desc()).all()
        return result

    # 切换文章的隐藏状态：1表示隐藏，0表示显示
    @staticmethod
    def switch_hidden(articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        if row.hidden == 1:
            row.hidden = 0
        else:
            row.hidden = 1
        dbsession.commit()
        return row.hidden  # 将当前最新状态返回给控制层

    # 切换文章的推荐状态：1表示推荐，0表示正常
    @staticmethod
    def switch_recommended(articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        if row.recommended == 1:
            row.recommended = 0
        else:
            row.recommended = 1
        dbsession.commit()
        return row.recommended

    # 切换文章的审核状态：1表示已审，0表示待审
    @staticmethod
    def switch_checked(articleid):
        row = dbsession.query(Article).filter_by(articleid=articleid).first()
        if row.checked == 1:
            row.checked = 0
        else:
            row.checked = 1
        dbsession.commit()
        return row.checked
