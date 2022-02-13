from typing import Optional, Awaitable

import tornado.web
import tornado
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
from conf.BaseHandler import BaseHandler
from common.models import (
    Customers,
    Orders,
    Dishes,
    Chooses
)

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


class LoginHandle(BaseHandler):
    """
        handle /customers/login request
        :param tableId: 顾客通过扫码识别到的桌号
    """
    customers_id = 0

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    def query_customer(self, table_id):
        # 根据桌号查看当天该桌是否有未结算订单，有返回已存在customer.id，没有返回0
        date = datetime.now().date()
        for ex_c in self.db.query(Customers).filter(Customers.date == date, Customers.tableId == table_id).all():
            if not ex_c.settlement:
                return ex_c.id
        return 0

    def get(self):
        try:
            # 获取⼊参
            table_id = self.get_argument('tableId')

            try:
                self.customers_id = self.query_customer(table_id)

                if not self.customers_id:
                    self.db.add(Customers(table_id))
                    self.db.commit()
                    self.customers_id = self.query_customer(table_id)

                # 返回顾客id
                data = {"customerId": self.customers_id}
                print(data.values())
                http_response(self, data, '0')
                # self.render('customerIndex.html')

            except Exception as e:
                self.db.rollback()
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR： {e}")

    def post(self):
        pass


def set_two_num(num):
    result = ''
    if num >= 10:
        result = result + str(num)
    else:
        result = result + '0' + str(num)
    return result


def set_id(c_id):
    id_ = c_id % 10000
    if id_ < 10:
        result = '000' + str(id_)
    elif id_ < 100:
        result = '00' + str(id_)
    elif id_ < 1000:
        result = '0' + str(id_)
    else:
        result = '' + str(id_)
    return result


def get_id(customer_id):
    # 根据用户id生成订单编号
    date = datetime.now()
    order_id = '' + str(date.year) + set_two_num(date.month) + set_two_num(date.month) + set_two_num(date.day) \
               + set_two_num(date.hour) + set_two_num(date.minute) + set_two_num(date.second)
    order_id = order_id + set_id(customer_id)
    return order_id


class SubmitHandle(BaseHandler):
    """
    handle /customers/submit request
    :param customer_id: 顾客编号
    :param dishes: 顾客点的菜品编号列表
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
            dishes = self.get_argument('dishes')

            try:
                customer_id = eval(customer_id)
                order_id = get_id(customer_id)
                order = Orders(order_id, customer_id, dishes)
                # 计算总价
                order.discount = 0
                total_price = 0
                dishes = eval(dishes)
                for dishes_id in dishes:
                    ex_d = self.db.query(Dishes).filter(Dishes.id == dishes_id).first()
                    if ex_d:
                        total_price += ex_d.price
                    else:
                        print('dishes_id:不存在！')
                order.totalPrice = total_price
                self.db.add(order)
                # choose表
                ex_c = self.db.query(Chooses).filter(Chooses.customerId == customer_id).first()
                if ex_c:
                    # self.db.delete(ex_c)
                    # self.db.commit()
                    order_list = eval(ex_c.orderIds)
                    order_list.append(order.id)
                    if order_list:
                        self.db.query(Chooses).filter(Chooses.id == ex_c.id).update({Chooses.orderIds: str(order_list)})
                        self.db.commit()
                    else:
                        print('order_list 不存在')
                else:
                    order_ids = [order.id]
                    choose = Chooses(customer_id, str(order_ids))
                    self.db.add(choose)
                    self.db.commit()
                data = {"orderId": order.id}
                # 返回订单编号
                http_response(self, data, '0')

            except Exception as e:
                self.db.rollback()
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR： {e}")


class OrdersHandler(BaseHandler):
    """
    顾客更新订单状态
    handle /customers/orders request
        :param customerId: 顾客id
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    def query_customer(self, table_id):
        # 根据桌号查看当天该桌是否有未结算订单，有返回已存在customer.id，没有返回0
        date = datetime.now().date()
        for ex_c in self.db.query(Customers).filter(Customers.date == date, Customers.tableId == table_id).all():
            if not ex_c.settlement:
                return ex_c.id
        return 0

    def get(self):
        pass

    def post(self):
        try:
            # 获取⼊参
            customer_id = self.get_argument('customerId')

            try:
                choose = self.db.query(Chooses).filter(Chooses.customerId == customer_id).first()
                order_ids = eval(choose.orderIds)
                orders = []
                for order_id in order_ids:
                    order = self.db.query(Orders).filter(Orders.id == order_id).first()
                    orders.append(order.to_dict())

                # 返回顾客id
                data = {"customerId": orders}
                http_response(self, data, '0')

            except Exception as e:
                self.db.rollback()
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['2001'], '2001')
            print(f"ERROR： {e}")
