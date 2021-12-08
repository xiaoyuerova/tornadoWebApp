from typing import Optional, Awaitable
from time import sleep

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
    Managers,
    Cashiers,
    CateringStaffs
)

# Configure logging,生成日志文件
logFilePath = "log/login/login.log"  # 日志保存地址
logger = logging.getLogger("login")
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


class RegisterHandler(tornado.web.RequestHandler):
    """
    handle /users/regist request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    # 管理员注册
    def case0(self, name, password):
        try:
            manager = self.db.query(Managers).filter(Managers.name == name).first()
            if manager:
                http_response(self, ERROR_CODE['1005'], '1005')
            else:
                ex_manager = Managers(name, password)
                self.db.add(ex_manager)
                self.db.commit()
                http_response(self, ERROR_CODE['1006'], '1006')
                sleep(2)
                self.render('login.html')

        except Exception as e:
            self.db.rollback()
            http_response(self, f"ERROR： {e}", '')
            print(f"ERROR： {e}")
        finally:
            self.db.close()

    # 配餐员注册
    def case1(self, name, password):
        try:
            catering_staff = self.db.query(CateringStaffs).filter(Managers.name == name).first()
            if catering_staff:
                http_response(self, ERROR_CODE['1005'], '1005')
            else:
                ex_catering = CateringStaffs(name, password)
                self.db.add(ex_catering)
                self.db.commit()
                http_response(self, ERROR_CODE['1006'], '1006')
                sleep(2)
                self.render('login.html')

        except Exception as e:
            self.db.rollback()
            http_response(self, f"ERROR： {e}", '')
            print(f"ERROR： {e}")
        finally:
            self.db.close()

    # 收银员注册
    def case2(self, name, password):
        try:
            cashier = self.db.query(Cashiers).filter(Managers.name == name).first()
            if cashier:
                http_response(self, ERROR_CODE['1005'], '1005')
            else:
                ex_cashier = Cashiers(name, password)
                self.db.add(ex_cashier)
                self.db.commit()
                http_response(self, ERROR_CODE['1006'], '1006')
                sleep(2)
                self.render('login.html')

        except Exception as e:
            self.db.rollback()
            http_response(self, f"ERROR： {e}", '')
            print(f"ERROR： {e}")
        finally:
            self.db.close()

    def default(self):
        http_response(self, ERROR_CODE['1004'], '1004')

    switch = {
        'case0': case0,
        'case1': case1,
        'case2': case2,
        'default': default
    }

    def get(self):
        self.render("regist.html")

    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            user_type = eval(self.get_argument('userType'))  # 用户类型：0：管理员，1：配餐员，2：收银员
            name = eval(self.get_argument('name'))
            password = eval(self.get_argument('password'))

            try:
                self.switch.get(get_key(user_type))(name, password)

            except Exception as e:
                self.db.rollback()
                http_response(self, f"ERROR： {e}", '')
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")


def get_key(user_type):
    if user_type == 0:
        return 'case0'
    elif user_type == 1:
        return 'case1'
    elif user_type == 2:
        return 'case2'
    else:
        return 'default'


class LoginHandler(tornado.web.RequestHandler):
    """
    handle /user/login request
    """

    @property
    def db(self):
        return self.application.db

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    # 管理员登录
    def case0(self, name, password):
        try:
            manager = self.db.query(Managers).filter(Managers.name == name).first()
            if manager.password == password:
                http_response(self, ERROR_CODE['0'], '0')
                self.render("managerIndex.html")
            else:
                http_response(self, ERROR_CODE['1002'], '1002')
        except Exception as e:
            http_response(self, ERROR_CODE['1003'], '1003')
            print(f"ERROR： {e}")

    # 配餐员登录
    def case1(self, name, password):
        try:
            catering_staff = self.db.query(CateringStaffs).filter(CateringStaffs.name == name).first()
            if catering_staff.password == password:
                http_response(self, ERROR_CODE['0'], '0')
                self.render("cateringStaffs.html")
            else:
                http_response(self, ERROR_CODE['1002'], '1002')
        except Exception as e:
            http_response(self, ERROR_CODE['1003'], '1003')
            print(f"ERROR： {e}")

    # 收银员登录
    def case2(self, name, password):
        try:
            cashier = self.db.query(Cashiers).filter(Cashiers.name == name).first()
            if cashier.password == password:
                http_response(self, ERROR_CODE['0'], '0')
                self.render("cashiers.html")
            else:
                http_response(self, ERROR_CODE['1002'], '1002')
        except Exception as e:
            http_response(self, ERROR_CODE['1003'], '1003')
            print(f"ERROR： {e}")

    def default(self):
        http_response(self, ERROR_CODE['1004'], '1004')

    switch = {
        'case0': case0,
        'case1': case1,
        'case2': case2,
        'default': default
    }

    def get(self):
        self.render("login.html")

    def post(self, *args, **kwargs):
        try:
            # 获取⼊参
            user_type = eval(self.get_argument('userType'))  # 用户类型：0：管理员，1：配餐员，2：收银员
            name = eval(self.get_argument('name'))
            password = eval(self.get_argument('password'))

            try:
                self.switch.get(get_key(user_type))(name, password)

            except Exception as e:
                self.db.rollback()
                http_response(self, f"ERROR： {e}", '')
                print(f"ERROR： {e}")
            finally:
                self.db.close()

        except Exception as e:
            # 获取⼊参失败时，抛出错误码及错误信息
            http_response(self, ERROR_CODE['1001'], '1001')
            print(f"ERROR： {e}")
