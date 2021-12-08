from __future__ import unicode_literals
from .customers_views import (
    LoginHandle,
    SubmitHandle,
    OrdersHandler
)

urls = [
    (r'login', LoginHandle),
    (r'submit', SubmitHandle),
    (r'orders', OrdersHandler)
]
