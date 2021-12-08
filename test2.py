from datetime import datetime
from datetime import timedelta


def main():
    date1 = datetime(2021, 1, 1)
    date2 = datetime(2021, 1, 4)
    date3 = datetime.strptime('2021-2-2', "%Y-%m-%d")  # "%Y-%m-%d %H:%M:%S.%f"
    print(date3 + timedelta(days=1))


if __name__ == '__main__':
    main()
