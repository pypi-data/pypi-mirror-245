#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import redis
from redis.exceptions import ConnectionError

from test_base_package.utils.logger import logger


class RedisDB:
    __conn = None

    def __init__(self, host="localhost", port=6379, password="123qwe"):
        self.host = host
        self.port = port
        self.password = password

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def connect(self):
        """连接数据数据"""
        try:
            self.__conn = redis.Redis(host=self.host, port=self.port, password=self.password, decode_responses=True)
        except ConnectionError as err:
            logger.error(err)
            raise "redis连接失败"
        except Exception as err:
            logger.error(err)
            raise err
        return self.__conn

    def close(self):
        """关闭连接"""
        if self.__conn:
            self.__conn.close()
