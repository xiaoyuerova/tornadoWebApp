from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:wxt123@localhost:3306/orderingSystem?charset=utf8', encoding="utf8", echo=False)
BaseDB = declarative_base()

# # 服务器端 IP+Port，请修改对应的IP
SERVER_HEADER = "http://127.0.0.1:8000"

# 本项目有5个模块，每个模块错误码分配1000个。0-999通用状态码；1000-1999为模块一使用，以此类推
ERROR_CODE = {
    "0": "ok",

    # customers 模块
    "2001": "入参非法!"
}
