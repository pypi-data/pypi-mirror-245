# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
if PyApiB.tryImportModule("bs4",installName="bs4"):
    from bs4 import BeautifulSoup


class HtmlU(PyApiB):
    """
    HTML相关
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def parseByFile(self, filePath)->BeautifulSoup:
        htmlStr = pyuc.fileU().produce().read_str(filePath)
        return self.parseByStr(htmlStr)
    
    def parseByStr(self, htmlStr)->BeautifulSoup:
        return BeautifulSoup(htmlStr, "html.parser")

