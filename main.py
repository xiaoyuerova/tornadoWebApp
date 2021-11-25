#!/usr/bin/env python
# coding: utf-8

import tornado.ioloop
import tornado.web
import os
import sys
from tornado.options import define, options
from common.url_router import include, url_wrapper
from views.login.login_views import LoginHandler

from common.models import init_db
from sqlalchemy.orm import scoped_session, sessionmaker
from conf.base import BaseDB, engine, SERVER_HEADER


class Application(tornado.web.Application):
    def __init__(self):
        init_db()
        handles = url_wrapper([
            (r"/login/", include('views.login.login_urls')),
            (r"/customers/", include('views.customers.customers_urls')),
            (r"/cateringStaffs/", include('views.cateringStaffs.cateringStaffs_urls')),
            # (r"/cashiers/", include('views.cashiers.cashiers_urls')),
            # (r"/managers/", include('views.managers.managers_urls'))
        ])
        handles.append((r"/", LoginHandler))
        settings = dict(
            debug=True,
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates")
        )
        tornado.web.Application.__init__(self, handles, **settings)
        self.db = scoped_session(sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False
        ))


if __name__ == '__main__':
    print("Tornado server is ready for service\r")
    print("run in " + SERVER_HEADER)
    tornado.options.parse_command_line()
    Application().listen(8000, xheaders=True)
    tornado.ioloop.IOLoop.instance().start()
