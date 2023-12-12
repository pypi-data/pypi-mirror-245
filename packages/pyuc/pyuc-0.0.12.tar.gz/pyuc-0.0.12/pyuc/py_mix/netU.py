# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import socket
import re
if PyApiB.tryImportModule("ping3", installName="ping3"):
    import ping3


class NetU(PyApiB):
    """
    网络相关操作工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def getLocalIp(self):
        """ 获取本机的局域网ip """
        return socket.gethostbyname(socket.gethostname())

    def ping(self, dest_addr: str, timeout: int = 4, unit: str = "s", src_addr: str = None, ttl: int = None, seq: int = 0, size: int = 56, interface: str = None):
        """ ping域名 """
        return ping3.ping(dest_addr, timeout, unit, src_addr, ttl, seq, size, interface)

        
