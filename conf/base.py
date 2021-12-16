from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:wxt123@localhost:3306/orderingSystem?charset=utf8', encoding="utf8", echo=False)
BaseDB = declarative_base()

# # 服务器端 IP+Port，请修改对应的IP
SERVER_HEADER = "http://127.0.0.1:8000"

# 本项目有5个模块，每个模块错误码分配1000个。0-999通用状态码；1000-1999为模块一使用，以此类推
ERROR_CODE = {
    "0": "ok",

    # login模块
    "1001": "入参非法!",
    "1002": "登录密码错误",
    "1003": "用户未注册",
    "1004": "用户类型非法",
    "1005": "该用户名已注册",
    "1006": "注册成功! 请重新登录，2秒后自动跳转登录页...",
    "1007": "用户名长度非法",
    "1008": "密码长度非法",

    # customers 模块
    "2001": "入参非法!",

    # cashiers 模块
    "4001": "入参非法!",

    # managers 模块
    "5001": "入参非法",
    "5002": "修改对象不存在"
}
