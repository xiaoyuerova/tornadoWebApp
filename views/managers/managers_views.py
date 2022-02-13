from typing import Optional, Awaitable

import tornado.web
from tornado.escape import json_decode
from datetime import datetime

import logging
from logging.handlers import TimedRotatingFileHandler

from common.commons import (
    http_response,
    get_dates
)
# 从配置⽂件中导⼊错误码
from conf.base import (
    ERROR_CODE,
)
from common.models import (
    Dishes,
    Orders
)
from conf.BaseHandler import BaseHandler

# Configure logging,生成日志文件
logFilePath = "log/managers/managers.log"  # 日志保存地址
logger = logging.getLogger("Managers")
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


class LoginHandler(BaseHandler):
    """
        handle /managers/login request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.render('managerIndex.html')

    def post(self, *args, **kwargs):
        pass


class DishesHandler(BaseHandler):
    """
        handle /managers/dishes request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        try:
            dishes = self.db.query(Dishes).all()
            data = []
            if dishes:
                for ex_d in dishes:
                    ex_d.description = ''
                    ex_d.picture = ''
                    if ex_d.specialPrice:
                        ex_d.specialPrice = 'true'
                    else:
                        ex_d.specialPrice = 'false'
                    data.append(ex_d.to_dict())
            else:
                print('dishes 不存在')
            http_response(self, str(data), '0')

        except Exception as e:
            self.db.rollback()
            http_response(self, f"ERROR： {e}", '')
            print(f"ERROR： {e}")
        finally:
            self.db.close()


class OrderHandler(BaseHandler):
    """
        handle /managers/order request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def post(self):
        try:
            # 获取⼊参
            start_date = self.get_argument('startDate')
            end_date = self.get_argument('endDate')

            try:
                dates = get_dates(start_date, end_date)
                order_list = []
                for date in dates:
                    print(date)
                    date = datetime.strptime(date, "%Y-%m-%d")
                    for order_ob in self.db.query(Orders).filter(Orders.date == date).all():
                        if order_ob and order_ob.state == 3:
                            order_ob.date = str(order_ob.date)
                            order_ob.time = str(order_ob.time)
                            order_ob.discount = 0
                            order_list.append(order_ob.to_dict())
                data = str(order_list)
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


class SearchHandler(BaseHandler):
    """
        handle /managers/search request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def verify(self, style, name, special_price, dish_id):
        return True

    def get(self):
        pass

    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            name = self.get_argument('name')
            dish_id = self.get_argument('dishId')
            style = self.get_argument('style')
            special_price = self.get_argument('specialPrice')

            try:
                if not dish_id == '':
                    dish_id = int(dish_id)
                if not style == '':
                    style = int(style)
                key_special = False  # key_special  true:使用special_price搜索；false：不使用
                if special_price == "true":
                    special_price = True
                    key_special = True
                if special_price == "false":
                    special_price = False
                    key_special = True
                if not self.verify(style, name, special_price, dish_id):  # 验证数据合法性
                    http_response(self, ERROR_CODE['5004'], '5004')
                    return

                ex_dishes = self.db.query(Dishes).all()
                ex_dishes_dict = []
                for item in ex_dishes:
                    ex_dishes_dict.append(item.to_dict())

                # 检索
                data = []
                for dish in ex_dishes_dict:
                    if dish['style'] == style or dish['name'] == name or dish['id'] == dish_id:
                        data.append(dish)
                        continue
                    if key_special and dish['specialPrice'] == special_price:
                        data.append(dish)

                http_response(self, data, '0')
                print('get search answer successful')

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


class ShowHandler(BaseHandler):
    """
        handle /managers/show request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        ex_dishes = self.db.query(Dishes).all()
        ex_dishes_dict = []
        for item in ex_dishes:
            ex_dishes_dict.append(item.to_dict())
        data = ex_dishes_dict
        http_response(self, data, '0')

    def post(self, *args, **kwargs):
        pass


class AddHandler(BaseHandler):
    """
        handle /managers/add request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def verify(self, style, name, price, special_price, quantity):
        pass

    def get(self):
        pass

    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            style = self.get_argument('style')
            name = self.get_argument('name')
            price = self.get_argument('price')
            special_price = self.get_argument('specialPrice')
            quantity = self.get_argument('quantity')

            try:
                style = int(style)
                price = float(price)
                if special_price == "true":
                    special_price = True
                else:
                    special_price = False
                quantity = int(quantity)
                self.verify(style, name, price, special_price, quantity)  # 验证数据合法性

                dish = Dishes(style, name, price)
                dish.specialPrice = special_price
                dish.quantity = quantity
                self.db.add(dish)
                self.db.commit()
                http_response(self, ERROR_CODE['0'], '0')
                print('dish add successful')

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


class ModifyHandler(BaseHandler):
    """
    handle /managers/modify request
    用'#0'表示成员不修改
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
            id_ = self.get_argument('id')
            style = self.get_argument('style')
            name = self.get_argument('name')
            price = self.get_argument('price')
            special_price = self.get_argument('specialPrice')
            quantity = self.get_argument('quantity')

            try:
                # id_ = int(id_)
                ex = self.db.query(Dishes).filter_by(id=id_).first()
                if not ex:
                    print('修改对象不存在')
                    http_response(self, ERROR_CODE['5002'], '5002')

                if style:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.style: style})
                if name:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.name: name})
                if price:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.price: price})
                if special_price:
                    if special_price == 'true':
                        special_price = True
                    if special_price == 'false':
                        special_price = False
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.specialPrice: special_price})
                if quantity:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.quantity: quantity})
                self.db.commit()
                http_response(self, ERROR_CODE['0'], '0')
                ex2 = self.db.query(Dishes).filter_by(id=id_).first()
                print('dish modify successful')

            except Exception as e:
                self.db.rollback()
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['5001'], '5001')
            print(f"ERROR： {e}")


class DeleteHandler(BaseHandler):
    """
        handle /managers/delete request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        pass

    def post(self):
        try:
            # 获取⼊参
            id_ = self.get_argument('id')

            try:
                ex = self.db.query(Dishes).filter(Dishes.id == id_).first()
                self.db.delete(ex)
                self.db.commit()
                http_response(self, ERROR_CODE['0'], '0')
                print('dish delete successful')

            except Exception as e:
                self.db.rollback()
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['5001'], '5001')
            print(f"ERROR： {e}")
