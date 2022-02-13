from __future__ import unicode_literals
from .cashiers_views import (
    OrderHandle,
    SettlementHandler
)

urls = [
    (r'order', OrderHandle),
    (r'settlement', SettlementHandler)
]