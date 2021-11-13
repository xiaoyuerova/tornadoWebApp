from __future__ import unicode_literals
from .login_views import (
    RegisterHandler,
    LoginHandler
)

urls = [
    (r'register', RegisterHandler),
    (r'login', LoginHandler)
]
