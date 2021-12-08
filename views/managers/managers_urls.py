from __future__ import unicode_literals
from .managers_views import (
    OrderHandler,
    ShowHandler,
    AddHandler,
    ModifyHandler,
    DeleteHandler
)

urls = [
    (r'order', OrderHandler),
    (r'show', ShowHandler),
    (r'add', AddHandler),
    (r'modify', ModifyHandler),
    (r'delete', DeleteHandler)
]
