import copy
from typing import Optional, Awaitable
import json

import tornado.web
from tornado.escape import json_decode

import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

from common.commons import (
    http_response,
    list_to_dict
)
# 从配置⽂件中导⼊错误码
from conf.base import (
    ERROR_CODE,
)
from common.models import (
    Customers,
    Chooses,
    Orders,
    Dishes
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


class OrderHandle(tornado.web.RequestHandler):
    """
    handle /cateringStaffs/order request
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
        try:
            date = datetime.now().date()
            customers = self.db.query(Customers).filter(Customers.date == date, Customers.settlement == False).all()

            chooses = []
            orders = []
            for customer in customers:
                choose = self.db.query(Chooses).filter(Chooses.customerId == customer.id).first()
                chooses.append(choose)
                for orderId in eval(choose.orderIds):
                    orders.append(self.db.query(Orders).filter(Orders.id == orderId).first())
            data = {
                "customers": str(list_to_dict(customers)),
                "choose": str(list_to_dict(chooses)),
                "orders": str(list_to_dict(orders))
            }

            http_response(self, data, '0')
            print('cateringStaffs order successful')

        except Exception as e:
            self.db.rollback()
            http_response(self, f"ERROR： {e}", '')
            print(f"ERROR： {e}")
        finally:
            self.db.close()

    def post(self):
        pass


class OperateHandler(tornado.web.RequestHandler):
    """
    handle /cateringStaffs/operate request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    def get(self):
        pass

    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            order_id = self.get_argument('orderId')

            try:
                # 0：已提交；1：正在配餐；2：已出餐；3：已结算
                self.db.query(Orders).filter(Orders.id == order_id).uptate({Orders.state: 1})
                self.db.commit()
                http_response(self, ERROR_CODE['0'], '0')

            except Exception as e:
                self.db.rollback()
                http_response(self, f"ERROR： {e}", '')
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['5001'], '5001')
            print(f"ERROR： {e}")


class CompleteHandler(tornado.web.RequestHandler):
    """
    handle /cateringStaffs/complete request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    def get(self):
        pass

    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            order_id = self.get_argument('orderId')

            try:
                # 0：已提交；1：正在配餐；2：已出餐；3：已结算
                self.db.query(Orders).filter(Orders.id == order_id).uptate({Orders.state: 2})
                self.db.commit()
                http_response(self, ERROR_CODE['0'], '0')

            except Exception as e:
                self.db.rollback()
                http_response(self, f"ERROR： {e}", '')
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['5001'], '5001')
            print(f"ERROR： {e}")
