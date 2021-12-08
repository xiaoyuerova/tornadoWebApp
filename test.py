from sqlalchemy.orm import sessionmaker
from datetime import datetime

from conf.base import (engine, BaseDB)

from common.commons import (
    list_to_dict
)

from common.models import (
    Customers,
    Chooses,
    Orders,
    Dishes,
)

dishes = [
    {
        "style": 2,  # 0：套餐；1：主餐；2：小吃；3：饮品
        "name": '薯条（大）',
        "price": 6,
        "quantity": 123
    },
    {
        "style": 2,  # 0：套餐；1：主餐；2：小吃；3：饮品
        "name": '薯条（小）',
        "price": 3,
        "quantity": 321
    },
    {
        "style": 2,  # 0：套餐；1：主餐；2：小吃；3：饮品
        "name": '劲爆鸡米花',
        "price": 4,
        "quantity": 41
    },
]


def main():
    # 这里单独控制数据库，比如操控记录
    Session = sessionmaker(bind=engine,
                           autocommit=False,
                           autoflush=True,
                           expire_on_commit=False)
    session = Session()

    # 这里写操作
    try:
        # 添加顾客数据
        # customer = Customers(1)
        # session.add(customer)
        # session.commit()

        # 查看当天顾客
        # date = datetime.now().date()
        # ex_customers = session.query(Customers).filter(Customers.date == date).all()
        # customer_dict = []
        # for item in ex_customers:
        #     customer_dict.append(item.to_dict())
        # print(customer_dict)

        # 添加Choose
        # for customer in session.query(Customers).all():
        #     # choose = session.query(Chooses).filter(Chooses.customerId == customer.id).first()
        #     choose = Chooses(customer.id, '[1,2]')
        #     session.add(choose)
        #     session.commit()
        # for choose in session.query(Chooses).all():
        #     order_ids = [str(choose.id)]
        #     session.query(Chooses).filter(Chooses.id == choose.id).update({Chooses.orderIds: str(order_ids)})
        # session.commit()
        # print(list_to_dict(session.query(Chooses).all()))

        # # 添加Dishes
        # for item in dishes:
        #     dishes_ = Dishes(item.get("style"), item.get("name"), item.get("price"))
        #     session.add(dishes_)
        # session.commit()
        # print(list_to_dict(session.query(Dishes).all()))

    except Exception as e:
        session.rollback()
        print(f"ERROR： {e}")
    finally:
        session.close()


if __name__ == '__main__':
    main()
