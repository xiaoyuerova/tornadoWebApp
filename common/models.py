from conf.base import (BaseDB, engine)
from datetime import datetime
import sys
from sqlalchemy import (
    Column,
    Float,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey
)


# class DbBase:
#     def __init__(self):
#         pass
#
#     def to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Customers(BaseDB):
    # table for customers
    __tablename__ = "customers"
    # 定义表结构
    id = Column(Integer, primary_key=True)
    tableId = Column(Integer, nullable=False, index=True)
    data = Column(DateTime, nullable=False, index=True)
    phoneNumber = Column(String(20), nullable=True)
    identify = Column(Integer, nullable=True)
    settlement = Column(Boolean, nullable=False)

    def __init__(self, tableId):
        self.tableId = tableId
        self.data = datetime.now()
        self.settlement = False

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Dishes(BaseDB):
    # table for dishes
    __tablename__ = "dishes"
    # 定义表结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    style = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    picture = Column(String(400), nullable=True)
    price = Column(Float, nullable=False)
    specialPrice = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)

    def __init__(self, style, name, price):
        self.style = style
        self.style = name
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

    def __init__(self, customerId, oderIds):
        self.customerId = customerId
        self.orderIds = oderIds

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def get_id(customer_id):
    # 这里要改，别忘了！！！
    # 这里要改，别忘了！！！
    # 这里要改，别忘了！！！
    oder_id = [customer_id]
    return ''.join(oder_id)


def get_total_price(dishes):
    # 这里要改，别忘了！！！
    # 这里要改，别忘了！！！
    # 这里要改，别忘了！！！
    return 10


class Orders(BaseDB):
    # table for orders
    __tablename__ = "orders"
    # 定义表结构
    id = Column(String(20), primary_key=True)
    customerId = Column(Integer, ForeignKey("customers.id"), nullable=False)
    dishes = Column(String(200), nullable=False)
    totalPrice = Column(Float, nullable=True)
    discount = Column(Float, nullable=True)
    state = Column(Integer, nullable=True)

    def __init__(self, customer_id, dishes):
        self.id = get_id(customer_id)
        self.customerId = customer_id
        self.dishes = dishes
        self.totalPrice = get_total_price(dishes)
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
        self.id += 100


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
