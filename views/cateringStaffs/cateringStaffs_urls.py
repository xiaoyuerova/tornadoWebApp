from __future__ import unicode_literals

from .cateringStaffs_views import (
    OrderHandle,
    OperateHandler,
    CompleteHandler
)

urls = [
    (r'order', OrderHandle),
    (r'operate', OperateHandler),
    (r'complete', CompleteHandler)
]
