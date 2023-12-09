"""
hashlib加密工具
"""
import hashlib
import os


def calc_unique_id(data_list: list, split_chat: str = '') -> str:
    """
    计算唯一id
    :param data_list: 字符串列表
    :param split_chat: 分割符
    :return:
    """
    return calc_md5(split_chat.join(data_list))


def calc_byte_md5(data_byte: bytes) -> str:
    """计算md5"""
    return hashlib.md5(data_byte).hexdigest()


def calc_md5(data_str: str) -> str:
    """计算md5"""
    return hashlib.md5(data_str.encode('utf-8')).hexdigest()


def calc_file_md5(data_file: str) -> str:
    """计算文件的md5"""
    with open(data_file, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest().lower()


def calc_file_slice_md5(data_file: str, slice_length: int = 256 * 1024) -> str:
    """文件校验段的MD5，32位小写，校验段对应文件前256KB"""
    if os.path.getsize(data_file) >= slice_length:
        with open(data_file, 'rb') as f:
            return hashlib.md5(f.read(slice_length)).hexdigest().lower()
    else:
        return calc_file_md5(data_file=data_file)
