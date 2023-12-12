# -*- coding: UTF-8 -*-
from pyuc.py_api_b import PyApiB
import os, socket


class EnvU(PyApiB):
    """
    环境变量相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def get(self,key,default=None):
        """ 获取环境变量的值 """
        value = default
        if key in os.environ:
            value = os.environ[key]
        return value

    def getLocalIp(self):
        """ 获取本机的局域网ip """
        return socket.gethostbyname(socket.gethostname())

    