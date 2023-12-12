# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import time
import os
from itertools import islice,takewhile,repeat



class FileQueueU(PyApiB):
    """
    文件做中间件的队列工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    @property
    def filePath(self):
        __filePath = getattr(self, "__filePath", None)
        if __filePath == None:
            __filePath = "."+os.sep+self._signKey
            setattr(self, "__filePath", __filePath)
        return __filePath

    @filePath.setter
    def filePath(self, path:str):
        setattr(self, "__filePath", path)

    def push(self, msg:str):
        with open(self.filePath, "a", encoding="utf-8") as pipe:
            if (not msg) or (not msg.endswith("\n")):
                pipe.write(f"{msg}\n")

    def __prapareFile__(self):
        if not os.path.exists(self.filePath):
            pyuc.fileU().write_str(self.filePath, "")
            # with open(self.filePath, "a", encoding="utf-8") as pipe:
            #     pipe.write(f"")

    def toList(self, startLine=0, endLine=999999999) -> list:
        """ 不增不减返回所有内容 """
        self.__prapareFile__()
        lines = []
        with open(self.filePath, "r+", encoding="utf-8") as pipe:
            lines = list(islice(pipe, startLine, endLine))
            # lines = pipe.readlines()
        return lines
    
    def count(self):
        self.__prapareFile__()
        buffer = 1024*1024
        with open(self.filePath, "r", encoding="utf-8") as pipe:
            buf_gen = takewhile(lambda x:x, (pipe.read(buffer) for _ in repeat(None)))
            return sum(buf.count("\n") for buf in buf_gen)

    def pop(self, isWait=True):
        """ 从队尾先出（先进先出） """
        data = None
        self.__prapareFile__()
        with open(self.filePath, "r+", encoding="utf-8") as pipe:
            lines = pipe.readlines()
            while isWait and (not lines):
                time.sleep(0.01)
                lines = pipe.readlines()
            if lines:
                data = lines[-1].rstrip()
                pipe.seek(0)
                pipe.writelines(lines[:-1])
                pipe.truncate()
        return data

    def popl(self, isWait=True):
        """ 从队尾先出（先进先出） """
        return self.pop(isWait)

    def poll(self, isWait=True):
        """ 从队头出（先进先晚） """
        data = None
        self.__prapareFile__()
        with open(self.filePath, "r+", encoding="utf-8") as pipe:
            lines = pipe.readlines()
            while isWait and (not lines):
                time.sleep(0.01)
                lines = pipe.readlines()
            if lines:
                data = lines[0].rstrip()
                pipe.seek(0)
                pipe.writelines(lines[1:])
                pipe.truncate()
        return data
