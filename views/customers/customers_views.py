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
from views.cateringStaffs.cateringStaffs_views import CaterHandle

# Configure logging,生成日志文件
logFilePath = "log/customers/customer.log"  # 日志保存地址
logger = logging.getLogger("customers")
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


class LoginHandle(tornado.web.RequestHandler):
    """
        handle /customers/login request
        :param tableId: 顾客通过扫码识别到的桌号
        response:
            "data":{type1:{},type2:{}}  对象转成的字典,以type为key区分并访问每一行
            "code":code
        """
    customers_id = 0
    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    def query_customer(self, table_id):
        # 根据桌号查看该桌是否有未结算订单，有返回已存在customer.id，没有返回0
        for ex_c in self.db.query(Customers).filter_by(tableId=table_id):
            if not ex_c.settlement:
                return ex_c.id
        return 0

    def get(self):
        self.render("login.html")

    def post(self):
        try:
            # 获取⼊参
            tableId = self.get_argument('tableId')

            try:
                self.render('orderIndex.html')
                self.customers_id = self.query_customer(tableId)

                if not self.customers_id:
                    self.db.add(Customers(tableId))
                    self.db.commit()
                    self.customers_id = self.query_customer(tableId)
                    print('save successful')

            except Exception as e:
                self.db.rollback()
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR： {e}")


class SubmitHandle(tornado.web.RequestHandler):
    """
        handle /customers/submit request
        :param customer_id: 顾客编号
        :param order_id: 顾客提交的订单编号
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
        pass

    def post(self):
        try:
            # 获取⼊参
            customer_id = self.get_argument('customerId')
            order_id = self.get_argument('orderId')

            # 存进表chooses

            CaterHandle.refresh_orders()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR： {e}")
