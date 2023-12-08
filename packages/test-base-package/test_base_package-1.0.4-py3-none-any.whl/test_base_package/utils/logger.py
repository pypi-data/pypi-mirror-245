# -*- coding: utf-8 -*-
import os.path

import logging
from pathlib import Path

import colorlog
from test_base_package.utils import time_util, sys_util
from test_base_package.utils.sys_util import get_base_dir


class LogHandler:
    def __init__(self, filename, level=logging.INFO):
        self.logger = logging.getLogger(filename)
        self.log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s  %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s',
            log_colors=self.log_colors_config)

        # 设置日志级别
        self.logger.setLevel(level)
        # 往屏幕上输出
        console_handler = logging.StreamHandler()

        file_handler = logging.FileHandler(filename=filename, mode='a', encoding='utf8')

        file_formatter = logging.Formatter('%(asctime)s  %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s')
        # 设置写入文件的格式
        file_handler.setFormatter(file_formatter)

        # 设置屏幕上显示的格式
        console_handler.setFormatter(formatter)

        # 把对象加到logger里
        self.logger.addHandler(console_handler)

        self.logger.addHandler(file_handler)


base_dir = get_base_dir()

log_file = os.path.join(base_dir, "logs", "%s.log" % time_util.current_date())

sys_util.create_file(log_file)

log_handler = LogHandler(log_file, level=logging.DEBUG)

logger = log_handler.logger
