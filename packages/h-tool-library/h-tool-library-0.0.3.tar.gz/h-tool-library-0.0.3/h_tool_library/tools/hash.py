"""
    基础加密
"""

import hashlib
from werkzeug.security import generate_password_hash, check_password_hash


def md5_(s: str) -> str:
    """
    数据 -> md5
    :return:
    """
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()


def password_encry(password: str) -> str:
    """
        对密码进行sha256 加密
    :param password:
    :return:
    """
    return generate_password_hash(password)


def check_encry_password(password: str, encry_pwd: str):
    """
        对密码进行校验，判断是否是相同密码
    :param password: 用户传递的密码
    :param encry_pwd: 加密后的密码
    :return:
    """
    return check_password_hash(encry_pwd, password)
