# -*- coding: utf-8 -*-
import os
from pathlib import Path


def get_base_dir() -> str:
    """
    获取项目根目录
    """
    base_dir = Path(__file__).resolve().parent.parent.parent

    return base_dir


def join_path(*path):
    """
    拼接路径
    :param args:
    :return:
    """
    return os.path.join(*path)


def is_file_exists(path: str) -> bool:
    """
    判断文件是否存在
    """
    if os.path.exists(path):
        return True
    return False


def is_dir_exists(path: str) -> bool:
    """
    判断目录是否存在
    """
    if os.path.isdir(path):
        return True

    return False


def create_dir(path: str) -> str:
    """
    判断目录是否存在
    """
    if os.path.isdir(path):
        return path

    return os.makedirs(path)


def create_file(path: str):
    # 判断文件是否存在
    if is_file_exists(path):
        return

    # 拆分目录
    dir_path, file_name = os.path.split(path)

    # 判断目录是否存在，不存在则创建目录
    if not is_dir_exists(dir_path):
        os.makedirs(os.path.dirname(path))

    # 创建文件
    with open(path, 'w'):
        pass
