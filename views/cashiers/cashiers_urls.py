from __future__ import unicode_literals
from .cashiers_views import (
    OrdersHandler,
    SettlementHandler
)

urls = [
    (r'show', OrdersHandler),
    (r'settlement', SettlementHandler)
]