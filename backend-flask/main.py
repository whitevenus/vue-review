import os
import pymysql

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

pymysql.install_as_MySQLdb()

app = Flask(__name__, static_url_path="/", static_folder="resource", template_folder="templates")
app.config["SECRET_KEY"] = os.urandom(24)

# 配置数据库连接操作
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/woniunote?charset=utf8'
# 指定SQLAlchemy跟踪数据的更新操作为False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 设置连接池大小，默认为5，此处设置为100
app.config['SQLALCHEMY_POOL_SIZE'] = 100

# 实例化数据库连接
db = SQLAlchemy(app)


if __name__ == '__main__':
    # 导入其他模块并进行注册
    from controller.index import *
    from controller.type import *
    from controller.user import *
    from controller.article import *
    from controller.favorite import *
    from controller.comment import *
    from controller.editor import *
    from controller.admin import *
    from controller.ucenter import *
    app.register_blueprint(index)
    app.register_blueprint(type_)
    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(favorite)
    app.register_blueprint(comment)
    app.register_blueprint(editor)
    app.register_blueprint(admin)
    app.register_blueprint(ucenter)

    app.run(debug=True)
