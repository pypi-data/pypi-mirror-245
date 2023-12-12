# -*- coding: utf-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import multiprocessing,os,time
from .config import config
from .memuCU import MEmuCU
import threading,random
if PyApiB.tryImportModule("psutil", installName="psutil"):
    import psutil

class MEmuCMU(PyApiB):

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.typeSign=None
        self.dvs = {}

    def createMEmuc(self):
        return MEmuCU()

    def devices(self, isAll=False, typeSign=None, isReloadCache=False):
        rp = os.popen(f'"{config.MEmu_PATH}\memuc" listvms')
        res = rp.readlines()
        rp.close()
        checkTypeSign = self.typeSign
        if typeSign:
            checkTypeSign = typeSign
        nums = []
        for r in res:
            rs = r.split(",")
            if len(rs[0].replace("\n",""))>0:
                mEmuc = self.dvs.get(rs[0],None)
                if not mEmuc:
                    newOne = self.createMEmuc().update(*rs)
                    if isAll or newOne.typeSign == checkTypeSign:
                        self.dvs[rs[0]] = newOne
                        nums.append(rs[0])
                else:
                    self.dvs[rs[0]].update(*rs)
                    if self.dvs[rs[0]].typeSign == checkTypeSign:
                        nums.append(rs[0])
        needDelNums = []
        for n in self.dvs:
            if n not in nums:
                needDelNums.append(n)
        for needDelNum in needDelNums:
            try:
                del self.dvs[needDelNum]
            except BaseException:
                pass
        return self.dvs

    def memuStop(self, d:MEmuCU):
        d.stop(saveCache=True)

    def memuStart(self, d:MEmuCU):
        d.start(isHide=config.isStartHideDevices)

    # def asyncMemuStart(self, d:MEmuCU):
    #     th = multiprocessing.Process(target=self.memuStart,args=(self,d,))
    #     # th = threading.Thread(target=self.memuStart,args=(d,))
    #     # th.setDaemon(True)
    #     th.start()

    def asyncMemuStop(self, d:MEmuCU):
        th = threading.Thread(target=self.memuStop,args=(d,))
        th.setDaemon(True)
        th.start()

    def fixSomeThs(self, dvs):
        return False

    def isProcessErr(self, p:psutil.Process):
        return False

    def killAllErrProcess(self):
        cs = psutil.process_iter()
        for c in cs:
            try:
                if self.isProcessErr(c):
                    os.system(f'tskill {c.pid}')
            except BaseException:
                pass


    def killAllOldProcess(self):
        cs = psutil.process_iter()
        for c in cs:
            try:
                if c.name() in ["RuntimeBroker.exe"]:
                    os.system(f'tskill {c.pid}')
            except BaseException:
                pass

        
    def start(self):
        self.killAllOldProcess()
        dvs = []
        try:
            while True:
                self.killAllErrProcess()
                time.sleep(3)
                dvs = self.devices()
                if self.fixSomeThs(dvs):
                    continue

                for dv in dvs:
                    d:MEmuCU = dvs[dv]
                    if d.isRunning == "1" and (not d.isOptionRunning()):
                        # 没有启动脚本
                        time.sleep(1)
                        d.asynLoopRunOption()
                runningCount = 0
                for dv in dvs:
                    d:MEmuCU = dvs[dv]
                    if d.isRunning == "1":
                        runningCount += 1
                print(runningCount,end="",flush=True)
                if runningCount < config.maxDeviceNum:
                    # 选一个设备来启动
                    if config.canDoAction("start",config.startInterval):
                        _canRuns = []
                        for dv in dvs:
                            d:MEmuCU = dvs[dv]
                            if d.canDeviceRun():
                                _canRuns.append(d)
                        if _canRuns:
                            self.memuStart(random.choice(_canRuns))
                if config.canDoAction("hideWindow",config.hideWindowCheckTime):
                    for dv in dvs:
                        d:MEmuCU = dvs[dv]
                        if d.isRunning == "1":
                            d.hideWindow()
                if config.canDoAction("reloadConfigFile",60):
                    config.loadConfigJson()
                    print("c",end="",flush=True)
        except BaseException:
            pass
        finally:
            for dId in dvs:
                dvs[dId].stopOption()

        