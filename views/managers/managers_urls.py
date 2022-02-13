from __future__ import unicode_literals
from .managers_views import (
    LoginHandler,
    OrderHandler,
    DishesHandler,
    ShowHandler,
    AddHandler,
    ModifyHandler,
    DeleteHandler,
    SearchHandler
)

urls = [
    (r'login', LoginHandler),
    (r'order', OrderHandler),
    (r'dishes', DishesHandler),
    (r'show', ShowHandler),
    (r'add', AddHandler),
    (r'modify', ModifyHandler),
    (r'delete', DeleteHandler),
    (r'search', SearchHandler)
]
