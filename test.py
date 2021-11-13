from sqlalchemy.orm import sessionmaker

from conf.base import (engine, BaseDB)


def main():
    # 这里单独控制数据库，比如操控记录
    Session = sessionmaker(bind=engine,
                           autocommit=False,
                           autoflush=True,
                           expire_on_commit=False)
    session = Session()

    # 这里写操作

    session.commit()
    session.close()


if __name__ == '__main__':
    main()
