"""
    基础函数
"""
import base64
import random
from io import BytesIO
from operator import itemgetter
from itertools import groupby
from typing import List, Dict, Any
from collections import Counter
import os
import re

from PIL import Image
from fake_useragent import UserAgent


def get_random_str(n: int) -> str:
    """
        生成n位随机数字符串
    :return:
    """
    return "".join([str(random.randint(0, 9)) for i in range(n)])


def get_img_info(img):
    """
        得到图片的size属性
    :param img:
    :return:
    """
    img_pillow = Image.open(img)
    return img_pillow.size


def img_to_base64(img):
    """
        图片转base64
    :param img:
    :return:
    """
    output_buffer = BytesIO()
    img.save(output_buffer, format='png')
    byte_data = output_buffer.getvalue()
    base64_str = 'data:image/png;base64,' + base64.b64encode(byte_data).decode('utf-8')
    return base64_str


def group_of_arr(rows: List[Dict], key: str):
    """
        对数组内的字典，进行排序并分组
        example:
            rows = [
                {"address": 'beijing', "date": "2020/7/1", "weather": "晴天"},
                {"address": 'shanghai', "date": "2020/7/1", "weather": "晴天"},
                {"address": 'beijing', "date": "2020/6/30", "weather": "多云"},
                {"address": 'wuhan', "date": "2020/7/1", "weather": "晴天"},
                {"address": 'wuhan', "date": "2020/6/29", "weather": "暴雨"},
            ]
            -> {
                "2020/6/29": [{"address": 'beijing', "date": "2020/6/30", "weather": "多云"}],
                "2020/6/30": [...]
            }
    :param rows: 数组内嵌套字典
    :param key: 排序字段
    :return:
    """
    result = {}
    rows.sort(key=itemgetter(key))  # 必须排序
    for k, items in groupby(rows, key=itemgetter(key)):
        result[k] = list(items)
    return result


def get_ele_count(arr: List[Any]):
    """
        获取元素的个数
    :param arr:
    :return:
    """
    counts = Counter(arr)
    return dict(counts)


def check_in_file(my_file: str, my_string: str):
    with open(my_file) as f:
        try:
            return my_string in f.read()
        except Exception as e:
            return False


def path_to_dict(path, exclude=None, my_string=None):
    """
        将路径下所有的文件和文件夹转为json值
    :param path: 解析路径
    :param exclude: 排序的文件夹
    :param my_string:
    :return:
    """
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = []
        d['path'] = path
        paths = [os.path.join(path, x) for x in os.listdir(path) if x not in exclude]
        # Just the children that contains at least a valid file
        for p in paths:
            c = path_to_dict(p, exclude, my_string)
            if c is not None:
                d['children'].append(c)
        if not d['children']:
            return None
    else:
        if my_string is not None and not check_in_file(path, my_string):
            return None
        d['type'] = "file"
        d['path'] = path
    return d


def strip_text(text):
    """
    去除字符串中的空格
    :param text:
    :return:
    """
    text = "".join(text.split(" ")).strip()
    text = re.sub('\n', '', text)
    return text


def clean_html(html: str):
    """
        处理html
    :param html:
    :return:
    """
    html = html.strip('"')
    html = html.replace('\\r', '').replace('\\n', '').replace('\\t', '')
    html = html.replace('\\"', '"').replace('\\/', '/')
    return html


def get_fake_useragent(browsers=None, os_list=None):
    """
        获取随机的浏览器请求头
    :return:
    """
    if browsers is None:
        browsers = ["chrome", "edge", "firefox", "safari"]
    if os_list is None:
        os_list = ["windows", "macos", "linux"]
    ua = UserAgent(browsers=browsers, os=os_list)
    return ua.random
