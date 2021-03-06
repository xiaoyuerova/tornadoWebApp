from abc import ABC

import tornado.web

from conf.base import (BaseDB, engine)
from datetime import datetime
import sys
from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    Date,
    Time,
    Boolean,
    ForeignKey
)


class Customers(BaseDB):
    # table for customers
    __tablename__ = "customers"
    # 定义表结构
    id = Column(Integer, primary_key=True)
    tableId = Column(Integer, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False, index=True)
    phoneNumber = Column(String(20), nullable=True)
    identify = Column(Integer, nullable=True)
    settlement = Column(Boolean, nullable=False)

    def __init__(self, tableId):
        self.tableId = tableId
        self.date = datetime.now().date()
        self.time = datetime.now().time()
        self.identify = 0
        self.settlement = False

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Dishes(BaseDB):
    # table for dishes
    __tablename__ = "dishes"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    style = Column(Integer, nullable=False)                 # 0：套餐；1：主餐；2：小吃；3：饮品
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    picture = Column(String(400), nullable=True)
    price = Column(Float, nullable=False)
    specialPrice = Column(Boolean, nullable=True)           # false:非特价；true:特价
    quantity = Column(Integer, nullable=True)

    def __init__(self, style, name, price):
        self.style = style
        self.name = name
        self.price = price

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Chooses(BaseDB):
    # table for chooses
    __tablename__ = "chooses"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    customerId = Column(Integer, ForeignKey("customers.id"), nullable=False)
    orderIds = Column(String(100), nullable=False)

    def __init__(self, customer_id, order_ids):
        self.customerId = customer_id
        self.orderIds = order_ids

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Orders(BaseDB):
    # table for orders
    __tablename__ = "orders"
    # 定义表结构
    id = Column(String(20), primary_key=True)
    customerId = Column(Integer, ForeignKey("customers.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    time = Column(Time, nullable=False, index=True)
    dishes = Column(String(200), nullable=False)
    totalPrice = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    state = Column(Integer, nullable=True)

    def __init__(self, order_id, customer_id, dishes):
        self.id = order_id
        self.customerId = customer_id
        self.dishes = dishes
        self.date = datetime.now().date()
        self.time = datetime.now().time()
        self.discount = 0
        self.state = 0

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CateringStaffs(BaseDB):
    # table for cateringStaffs
    __tablename__ = "cateringStaffs"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class CompleteCaterings(BaseDB):
    # table for completeCaterings
    __tablename__ = "completeCaterings"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    cateringStaffId = Column(Integer, ForeignKey("cateringStaffs.id"), nullable=False, )
    oderId = Column(String(20), ForeignKey("orders.id"), nullable=False, )

    def __init__(self, catering_staff_id, oder_id):
        self.cateringStaffId = catering_staff_id
        self.oderId = oder_id


class Cashiers(BaseDB):
    # table for cashiers
    __tablename__ = "cashiers"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)

    def __init__(self, name, pwd):
        self.name = name
        self.password = pwd


class CompleteSettlement(BaseDB):
    # table for completeSettlement
    __tablename__ = "completeSettlement"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    cashierId = Column(Integer, ForeignKey("cashiers.id"), nullable=False, )
    customerId = Column(Integer, ForeignKey("customers.id"), nullable=False, )

    def __init__(self, cashierId, customerId):
        self.cashierId = cashierId
        self.customerId = customerId


class Managers(BaseDB):
    # table for managers
    __tablename__ = "managers"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    password = Column(String(20), nullable=False)

    def __init__(self, name, pwd):
        self.name = name
        self.password = pwd


def init_db():
    BaseDB.metadata.create_all(engine)


if __name__ == '__main__':
    print("Initialize database")
    init_db()
