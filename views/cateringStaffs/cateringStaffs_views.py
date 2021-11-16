from typing import Optional, Awaitable

import tornado.web
from tornado.escape import json_decode

import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from common.commons import (
    http_response,
)
# 从配置⽂件中导⼊错误码
from conf.base import (
    ERROR_CODE,
)
from common.models import (
    Customers,

)

# Configure logging,生成日志文件
logFilePath = "log/cateringStaffs/cateringStaffs.log"  # 日志保存地址
logger = logging.getLogger("cateringStaffs")
logger.setLevel(logging.DEBUG)
# 保留⽅式（这⾥设定按天保存，保留 30 天的 log 记录）
handler = TimedRotatingFileHandler(
    logFilePath,
    when="D",
    interval=1,
    backupCount=30
)
formatter = logging.Formatter('%(asctime)s\%(filename)s[line:%(lineno)d]%(levelname)s%(message)s', )
handler.suffix = "%Y%m%d"
handler.setFormatter(formatter)
logger.addHandler(handler)


class CaterHandle(tornado.web.RequestHandler):
    """
    handle /cateringStaffs/index request
    response:
        "data":{type1:{},type2:{}}  对象转成的字典,以type为key区分并访问每一行
        "code":code
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    def get(self):
        self.render("cateringStaffs.html")

    def post(self):
        pass
