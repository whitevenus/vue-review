from sqlalchemy import MetaData


# 直接将db实例导入，并返回在模型类中需要使用到的对象
def dbconnect():
    from main import db
    dbsession = db.session
    DBase = db.Model
    metadata = MetaData(bind=db.engine)
    return dbsession, metadata, DBase


# 将SQLAlchemy的结果集转换为列表+字典，返回[{},{}]格式
def model_list(result):
    list_ = []   # 定义列表用于存放所有行
    for item in result:
        # print(item._fields)
        dict_item = {}
        cnt = 0
        for row in item:
            # print(row)
            cnt += 1
            dict_ = {}   # 定义字典用于存放一行
            for k, v in row.__dict__.items():   # 遍历列名
                if not k.startswith('_sa_instance_state'):  # 跳过内置字段
                    dict_[k] = v
            if cnt == 1:
                dict_item["article"] = dict_
            elif cnt == 2:
                dict_item["user"] = dict_
        list_.append(dict_item)
    return list_


# 将SQLAlchemy的结果集转换为列表+字典，返回[{},{}]格式
def model_list_single(result):
    list_res = []
    for row in result:
        dict_ = {}   # 定义字典用于存放一行
        for k, v in row.__dict__.items():   # 遍历列名
            if not k.startswith('_sa_instance_state'):  # 跳过内置字段
                dict_[k] = v
        list_res.append(dict_)
    return list_res
