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
    Dishes,

)

# Configure logging,生成日志文件
logFilePath = "log/managers/managers.log"  # 日志保存地址
logger = logging.getLogger("manager")
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


class ShowHandler(tornado.web.RequestHandler):
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


class AddHandler(tornado.web.RequestHandler):
    """
        handle /managers/add request
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
            style = self.get_argument('style')
            name = self.get_argument('name')
            price = self.get_argument('price')
            specialPrice = self.get_argument('specialPrice')
            quantity = self.get_argument('quantity')

            try:
                dish = Dishes(style, name, price)
                dish.specialPrice = specialPrice
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


class ModifyHandler(tornado.web.RequestHandler):
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
            specialPrice = self.get_argument('specialPrice')
            quantity = self.get_argument('quantity')

            try:
                ex = self.db.query(Dishes).filter_by(id=id).first()
                if not ex:
                    print('修改对象不存在')
                    http_response(self, ERROR_CODE['5002'], '5002')

                if style:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.style: style})
                if name:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.name: name})
                if price:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.price: price})
                if specialPrice:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.specialPrice: specialPrice})
                if quantity:
                    self.db.query(Dishes).filter(Dishes.id == id_).update({Dishes.quantity: quantity})
                self.db.commit()
                http_response(self, ERROR_CODE['0'], '0')
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


class DeleteHandler(tornado.web.RequestHandler):
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
                ex = self.db.query(Dishes).filter(Dishes.id == id).first()
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
