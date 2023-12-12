# -*- coding: utf-8 -*-
import os, json, time


class Config:
    startInterval:int = 300
    MEmu_PATH:str="xxxx/MEmu"
    optionTimesConfig = {"fq_ylsxgbsygsf": {"times":7, "during": 7, "perTime": 7200}} # 这里改不会生效
    """ 操作次数限制：{optionKey:{times:次数， during: 多少天内, perTime: 一次跑多少秒}} """
    maxDeviceNum = 5
    """ 最多同时启动的设备数量 """
    maxAddBookNum = 1
    """ 最多同时启动添加书数量 """
    whenEndDoType:int = 1
    """ 读完时，要重新开始读0，还是直接结束1 """
    hideWindowCheckTime:int = 60
    """ 定时最小化所有视图的时间间隔 """
    isStartHideDevices:bool = True

    def __getDefaultConfig__(self):
        return {
            "startInterval": 300,
            "maxDeviceNum": 5,
            "maxAddBookNum": 1,
            "whenEndDoType": 1,
            "hideWindowCheckTime": -1,
            "isStartHideDevices": True,
            "optionTimesConfig": {"fq_ylsxgbsygsf": {"times":1, "during": 1,"perTime": 7200}},
        }
    

    def __init__(self):
        self.MEmu_PATH = os.environ.get("MEmu_PATH")
        if not self.MEmu_PATH:
            raise RuntimeError("Please add MEmu_PATH first!")
        self.loadConfigJson()
        self.lastDoTimes = {}
        self.hasDones = []
        

    def loadConfigJson(self):
        """ 加载配置的json """
        configJson = None
        try:
            with open('config.json', 'r') as f:
                configJson = json.load(f)
        except BaseException:
            pass
        tempC = self.__getDefaultConfig__()
        hasChange = False
        if not configJson:
            configJson = tempC
            hasChange = True
        for key in tempC:
            if key not in configJson:
                configJson[key] = tempC[key]
                hasChange = True
        for key in configJson:
            if configJson.get(key) != None:
                setattr(self, key, configJson[key])
        if hasChange:
            self.saveConfigJson()

    
    def saveConfigJson(self):
        with open('config.json', 'w',encoding='utf-8') as f:
            json.dump(self,ensure_ascii=False,default=lambda obj:obj.__dict__,fp=f,indent=2)

    def __str__(self) -> str:
        return json.dumps(self,ensure_ascii=False,default=lambda obj:obj.__dict__)
    

    def canDoAction(self, sign, timeout=1, isTrueRM=False, isFiltFirst=False):
        if timeout == -1:
            return False
        now = time.time()
        dd = self.lastDoTimes.get(sign,0)
        if dd == 0:
            self.lastDoTimes[sign] = now
            return not isFiltFirst
        if now - dd > timeout:
            if isTrueRM:
                try:
                    del self.lastDoTimes[sign]
                except BaseException:
                    pass
            else:
                self.lastDoTimes[sign] = now
            return True
        return False 
    
    
    def hasDone(self, sign):
        if sign not in self.hasDones:
            self.hasDones.append(sign)
            return False
        else:
            return True
    
    def isSameTimeDuring(self, t1, t2, tz_count=28800,during=86400):
        return int((int(t1)+int(tz_count))/during) == int((int(t2)+int(tz_count))/during)
    
    
config = Config()
