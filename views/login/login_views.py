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
logFilePath = "log/login/login.log"     # 日志保存地址
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
    :param phone: users sign up phone
    :param password: users sign up password
    digital code
    """

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        # 这是父类要求必须定义的，有什么用，没查过
        pass

    def get(self):
        self.render("register.html")


class LoginHandler(tornado.web.RequestHandler):
    """
    handle /user/login request
    response:
        "data":{type1:{},type2:{}}  对象转成的字典,以type为key区分并访问每一行
        "code":code
    """

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        print('login get')
        self.render("login.html")

    def post(self, *args, **kwargs):
        # user = self.get_body_argument('user')
        # pwd = self.get_body_argument('pwd')
        # if user == 'alex' and pwd == '123':
        #     self.set_secure_cookie('xxxxx', user)
        #     self.redirect('/index')
        #     return
        self.render('login.html', error='用户名或密码错误')
