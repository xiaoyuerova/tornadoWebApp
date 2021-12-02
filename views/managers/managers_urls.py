from __future__ import unicode_literals
from .managers_views import (
    ShowHandler,
    AddHandler,
    ModifyHandler,
    DeleteHandler
)

urls = [
    (r'show', ShowHandler),
    (r'add', AddHandler),
    (r'modify', ModifyHandler),
    (r'delete', DeleteHandler)
]
