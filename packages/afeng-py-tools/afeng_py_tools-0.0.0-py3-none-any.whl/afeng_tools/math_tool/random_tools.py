"""
Random随机数工具
"""
import random
import string
import time


def random_str(length: int = 5):
    """
    返回由【时间戳-length位随机字符】组成的字符串
    :param length: 随机字符长度
    :return: 【时间戳-length位随字符】组成的字符串
    """
    tmp_random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return str(time.time()) + '-' + tmp_random_str


def random_number_str(length: int = 6):
    """获取随机数字字符串"""
    return ''.join(random.choices(string.digits, k=length))


def random_state(length: int = 8):
    """获取随机生成的state"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)).lower()

