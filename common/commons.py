import json
import os
import datetime
from datetime import timedelta


def http_response(self, msg, code):
    """
    response:
            "data":{type1:{},type2:{}}  对象转成的字典,以type为key区分并访问每一行
            "code":code
    """
    self.write(json.dumps({"data": {"msg": msg, "code": code}}))


def save_files(file_metas, in_rel_path, type='image'):
    """
    Save file stream to server
    :param file_metas:
    :param in_rel_path:
    :param type:
    :return:
    """
    file_path = ""
    file_name_list = []
    for meta in file_metas:
        file_name = meta['filename']
        file_path = os.path.join(in_rel_path, file_name)
        file_name_list.append(file_name)
        # save image as binary
        with open(file_path, 'wb') as up:
            up.write(meta['body'])
    return file_name_list


def list_to_dict(object_list):
    """
    将数据库存储格式的对象列表转换为字典列表
    :param object_list: 对象列表（数据行列表）
    :return: 字典列表
    """
    dict_list = []
    for item in object_list:
        dict_list.append(item.to_dict())
    return dict_list


def get_dates(start_date, end_date):
    """
    获取时间段内每一天的日期
    :param start_date: 开始日期，字符串格式
    :param end_date: 终止日期，字符串格式
    :return: 时间段内每一天的日期列表
    """
    date_list = []
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while start <= end:
        date_str = start.strftime("%Y-%m-%d")
        date_list.append(date_str)
        start += timedelta(days=1)
    return date_list


if __name__ == "__main__":
    http_response()