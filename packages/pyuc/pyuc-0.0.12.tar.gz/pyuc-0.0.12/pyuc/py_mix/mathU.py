# -*- coding: UTF-8 -*-
from pyuc.py_api_b import PyApiB
import random
if PyApiB.tryImportModule("numpy", installName="numpy"):
    import numpy as np


class MathU(PyApiB):
    """
    数学相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def random(self, min=None, max=None, step=None):
        """
        生成一个随机数\n
        @Args:\n min：最小范围\n max: 最大范围\n step:随机步进范围\n
        """
        if min == None and max == None and step == None:
            return random.random()
        elif step == None:
            if isinstance(min, int) or isinstance(max, int):
                return random.randint(min, max)
            else:
                return random.uniform(min, max)
        else:
            return random.randrange(min, max, step)
          
    def randomArr(self, fromArr=None, getNum=0):
        if getNum==0 or fromArr == None or getNum >= len(fromArr):
            return []
        aa = []
        l = len(fromArr)
        while True:
            r = self.random(min=0,max=l-1)
            if fromArr[r] not in aa:
                aa.append(fromArr[r])
                if len(aa) == getNum:
                   break
        return sorted(aa)

    def __fitDatas(self, datas, key=None):
        if key != None:
            newDatas = list(map(lambda x:x[key],datas))  
            return self.__fitDatas(newDatas, None)
        return datas

    def aver(self, datas, key=None, maxNum=20):
        """ 平均值 """
        datas = self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        return np.mean(datas[-size:])
    
    def std(self, datas, key=None, maxNum=20):
        """ 标准差 """
        datas = self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        return np.std(datas[-size:])
    
    def boll(self, datas, key=None, maxNum=20):
        """ 布林 """
        datas= self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        mid = self.aver(datas[-size:])
        std = self.std(datas[-size:])
        top = mid + std + std
        bot = mid - std - std
        return [top, mid, bot]

    def rsi(self, datas, key=None, maxNum=14):
        t = self.__fitDatas(datas, key)
        length = len(t)
        rsies = [np.nan]*length
        #数据长度不超过周期，无法计算；
        if length <= maxNum:
            return rsies
        #用于快速计算；
        up_avg = 0
        down_avg = 0
    
        #首先计算第一个RSI，用前maxNum+1个数据，构成maxNum个价差序列;
        first_t = t[:maxNum+1]
        for i in range(1, len(first_t)):
            #价格上涨;
            if first_t[i] >= first_t[i-1]:
                up_avg += first_t[i] - first_t[i-1]
            #价格下跌;
            else:
                down_avg += first_t[i-1] - first_t[i]
        up_avg = up_avg / maxNum
        down_avg = down_avg / maxNum
        rs = up_avg / down_avg
        rsies[maxNum] = 100 - 100/(1+rs)
    
        #后面的将使用快速计算；
        for j in range(maxNum+1, length):
            up = 0
            down = 0
            if t[j] >= t[j-1]:
                up = t[j] - t[j-1]
                down = 0
            else:
                up = 0
                down = t[j-1] - t[j]
            #类似移动平均的计算公式;
            up_avg = (up_avg*(maxNum - 1) + up)/maxNum
            down_avg = (down_avg*(maxNum - 1) + down)/maxNum
            if down_avg != 0:
                rs = up_avg/down_avg
                rsies[j] = 100 - 100/(1+rs)
            else:
                rsies[j] = rsies[j-1]
        return rsies 

    
    def min(self, datas, key=None, maxNum=20):
        """ 最小值 """
        datas= self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        return min(datas[-size:])
        
    def max(self, datas, key=None, maxNum=20):
        """ 最大值 """
        datas= self.__fitDatas(datas, key)
        size = min(len(datas), maxNum)
        return max(datas[-size:])
    
    def MACD_EMA(self, preEMA, price, dayNums):
        """ EMA值 """
        # EMA(12)=前一日EMA(12)×11/13+今日收盘价×2/13
        return preEMA*(dayNums-1)/(dayNums+1)+price*2/(dayNums+1)
    
    def MACD(self, price, preDEA=0, preEMA12=0, preEMA26=0):
        """ 
        获取MACD的三个值:BAR(MACD),DIF,DEA
        返回：BAR(MACD),DIF,DEA,EMA12,EMA26
        """
        EMA12 = self.MACD_EMA(preEMA12, price, 12)
        EMA26 = self.MACD_EMA(preEMA26, price, 26)
        DIF = EMA12 - EMA26
        # 今日DEA(MACD)=前一日DEA×8/10+今日DIF×2/10
        DEA = preDEA*8/10+DIF*2/10
        BAR = 2*(DIF-DEA)
        return BAR,DIF,DEA,EMA12,EMA26
    
    