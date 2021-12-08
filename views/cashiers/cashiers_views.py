from typing import Optional, Awaitable

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
    Orders
)

# Configure logging,生成日志文件
logFilePath = "log/cashiers/cashier.log"  # 日志保存地址
logger = logging.getLogger("Cashier")
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


class OrdersHandler(tornado.web.RequestHandler):
    """
        handle /cashiers/orders request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        try:
            # 获取⼊参
            date = self.get_argument('date')

            try:
                # 查看当天顾客
                ex_customers = self.db.query(Customers).filter(Customers.date == date).all()
                # 查看当天顾客提交的订单并汇总
                chooses = []
                for customer in ex_customers:
                    temp_choose = self.db.query(Chooses).filter(Chooses.id == customer.id).first()
                    chooses.append(temp_choose)
                # 查询订单
                orders = self.db.query(Orders).filter(Orders.date == date).all()

                data = {
                    "customers": list_to_dict(ex_customers),
                    "chooses": list_to_dict(chooses),
                    "orders": list_to_dict(orders)
                }
                http_response(self, data, '0')

            except Exception as e:
                self.db.rollback()
                http_response(self, f"ERROR： {e}", '')
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['4001'], '4001')
            print(f"ERROR： {e}")

    def post(self):
        pass


class SettlementHandler(tornado.web.RequestHandler):
    """
        handle /cashiers/settlement request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        pass

    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            order_id = self.get_argument('orderId')

            try:
                self.db.query(Orders).filter(Orders.id == order_id).update({Orders.state: 3})
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
            http_response(self, ERROR_CODE['4001'], '4001')
            print(f"ERROR： {e}")
