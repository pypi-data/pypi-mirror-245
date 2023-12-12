# -*- coding: utf-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import os,time
from .config import config
from .optionBU import OptionBU
import json
import threading
import inspect
import ctypes
import random
import multiprocessing
if PyApiB.tryImportModule("psutil", installName="psutil"):
    import psutil
if PyApiB.tryImportModule("win32gui", installName="pywin32"):
    import win32gui,win32con


class MEmuCU(PyApiB):
    __cachePath__ = "./cache/devices"

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        self.num = None
        """ 索引 """
        self.title = None
        """ 标题 """
        self.handle = None
        """ 顶层窗口句柄 """
        self._isRunning = multiprocessing.Value('c')
        """ 是否启动模拟器 """
        self.pid = None
        """ 进程PID 信息 """
        self.adbDevice = None
        """ adb对应的设备名 """
        self.finishTimes = {}
        """ 完成的时间记录 """
        self.option:OptionBU = None
        """ 对应的操作实例 """
        self.optionThread:multiprocessing.Process = None
        """ 对应的操作线程 """
        self.typeSign:str = None
        """ 设备所属类型 """
        # self.__asynLoopRunOption = multiprocessing.Value('i',1)

        self.initOption()

    @property
    def isRunning(self):
        try:
            return self._isRunning.value.decode("utf-8")
        except BaseException:
            return None

    @isRunning.setter
    def isRunning(self, value):
        self._isRunning.value = value.encode("utf-8")

    def initOption(self):
        self.option = OptionBU()

    def updateFinishTimes(self):
        """ 操作完成了，更新完成时间 """
        signKey = self.option.signKey
        lastFishedTimes = self.finishTimes.get(signKey,[])
        if len(lastFishedTimes) > 10:
            lastFishedTimes = lastFishedTimes[-10:]
        lastFishedTimes.append(time.time())
        self.finishTimes[signKey] = lastFishedTimes
          
    def showWindow(self):
        try:
            if self.handle:
                win32gui.ShowWindow(int(self.handle),win32con.SW_SHOW)
        except BaseException:
            print("Error showWindow!")

    def hideWindow(self):
        try:
            print("H",end="",flush=True)
            if self.handle:
                win32gui.ShowWindow(int(self.handle),win32con.SW_HIDE)
        except BaseException:
            print("Error hideWindow!")

    def update(self, num=None, title=None, handle=None, isRunning=None, pid=None):
        if num == None or len(num.replace("\n",""))<=0:
            return
        if num != None:
            _num = num.replace("\n","")
            if _num.isalnum():
                self.num = _num
        if self.num != None and len(self.num) > 0:
            self.loadCache()
        if title != None:
            self.title = title.replace("\n","")
        
        if self.title and (self.title.startswith("B_") or self.title.startswith("C_")):
            self.typeSign = None
        elif self.title and self.title.startswith("A_"):
            self.typeSign = "addBook"
        else:
            self.typeSign = "others"
        if handle != None:
            self.handle = handle.replace("\n","")
        if isRunning != None:
            self.isRunning = isRunning.replace("\n","")
        if pid != None:
            self.pid = pid.replace("\n","")
        if self.num != None and len(self.num) > 0:
            self.saveCache()
        return self 
    
    def isFinishJobToday(self):
        """ 该设备今天的工作完成吗？ """
        signKey = self.option.signKey
        lastFishedTimes = self.finishTimes.get(signKey,[])
        otC = config.optionTimesConfig.get(signKey,{})
        nowTime = time.time()
        _times = 0
        for lft in lastFishedTimes:
            if config.isSameTimeDuring(nowTime,lft,during=86400*otC.get("during",1)):
                _times += 1
        if _times < otC.get("times",1):
            return False
        else:
            return True


    def canDeviceRun(self):
        """ 该设备今天还能用吗？ """
        if self.isRunning != "1":
            return not self.isFinishJobToday()
        return False


    def __str__(self) -> str:
        return json.dumps(self,ensure_ascii=False,default=lambda obj:self.__filtDictJson(obj.__dict__))

    def __filtDictJson(self, dictData):
        """ 将不需要传化为json的键去掉 """
        newData = {**dictData}
        if "option" in newData:
            del newData["option"]
        if "optionThread" in newData:
            del newData["optionThread"]
        if "_isRunning" in newData:
            del newData["_isRunning"]
        if "hack" in newData:
            del newData["hack"]
        return newData

    def saveCache(self):
        if not os.path.exists(self.__cachePath__):
            os.makedirs(self.__cachePath__)
        with open(f'{self.__cachePath__}/{self.num}.json', 'w',encoding='utf-8') as f:
            # print(self.__dict__)
            json.dump(self,ensure_ascii=False,default=lambda obj:self.__filtDictJson(obj.__dict__),fp=f,indent=2)

    def loadCache(self, num=None):
        lJson = self.loadCacheJson(num)
        lJson = self.__filtDictJson(lJson)
        if lJson:
            for key in lJson:
                if not key.startswith("_"):
                    setattr(self, key, lJson[key])

    def loadCacheJson(self, num=None):
        if num == None:
            num = self.num
        lJson = {}
        try:
            with open(f'{self.__cachePath__}/{self.num}.json', 'r',encoding='utf-8') as f:
                lJson = json.load(f)
        except BaseException:
            pass
        return lJson
    
    def isJsonMarkFinish(self, jsonData:dict):
        """ 是否json数据表示已经读完了 """
        return False

    def __run_cmd(self, cmd, timeout=None):
        import subprocess
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout,encoding="cp437")
            resText = result.stdout
            res = []
            if resText:
                res = resText.split("\n")
            return res
        except subprocess.TimeoutExpired:
            return []  # 返回空值表示超时

    def __asyn_run_cmd(self, cmd, timeout=None, asyncReturn=None):
        res = self.__run_cmd(cmd, timeout)
        if asyncReturn:
            asyncReturn(res)


    def run_command(self, command, timeout=None, asyncReturn=None):
        if asyncReturn:
            th = threading.Thread(target=self.__asyn_run_cmd,args=(command, timeout, asyncReturn,))
            th.setDaemon(True)
            th.start()
            return th
        else:
            return self.__run_cmd(command, timeout)

    def getMemucPath(self):
        return f"{config.MEmu_PATH}\memuc"

    def __memucCMDFixReturn(self, res, checkTexts):
        if not checkTexts:
            return res
        else:
            for r in res:
                print(r)
                if all(list(map(lambda ckt:ckt in r,checkTexts))):
                    return True
            return False

    def memucCMD(self, cmd, *checkTexts, asynCallBack=None, timeOut=None):
        runCMD = f'"{self.getMemucPath()}" {cmd}'
        print(runCMD)
        if asynCallBack == None:
            res = self.run_command(runCMD,timeout=timeOut)
            return self.__memucCMDFixReturn(res, checkTexts)
        else:
            def asyncReturn(res):
                rs = self.__memucCMDFixReturn(res, checkTexts)
                asynCallBack(rs)
            return self.run_command(runCMD, timeout=timeOut, asyncReturn=asyncReturn)

    @property
    def cmd_i_n(self):
        if self.num == None and self.title:
            res = self.memucCMD("listvms")
            for r in res:
                if r and "," in r:
                    rs = r.split(",")
                    if rs[1] == self.title:
                        self.num = rs[0]
                        break
        if self.num != None:
            return f"-i {self.num}"
        elif self.title != None:
            return f"-n {self.title}"

    def start(self, isHide=False):
        """ 启动 """
        self.stopOption()
        self.optionThread = None

        def onStartReturn(res):
            if res:
                self.refreshState()
                if isHide:
                    self.hideWindow()
            else:
                self.stop()
        
        self.memucCMD(f'start {self.cmd_i_n}', "SUCCESS: start vm finished.", timeOut=240, asynCallBack=onStartReturn)


    def isaudioPlaying(self):
        res = self.adbShell("dumpsys media_session",isPrint=False)
        # if self.num == "5":
        #     for r in res:
        #         print(r)
        for i in range(1,len(res)):
            r = res[i]
            if "state=PlaybackState" in r:
                if "state=3" in r:
                    return True
        return False
        
    def adbShell(self, cmd, isPrint=True):
        if self.adbDevice:
            adbCmd = f'adb -s {self.adbDevice} shell {cmd}'
            if isPrint:
                print(adbCmd)
            return self.run_command(adbCmd)
        else:
            return []

    def adbPull(self, fromPath, savePath):
        if self.adbDevice:
            adbCmd = f'adb -s {self.adbDevice} pull {fromPath} {savePath}'
            print(adbCmd)
            return self.run_command(adbCmd)
        else:
            return []

    def adbPush(self, fromPath, savePath):
        if self.adbDevice:
            adbCmd = f'adb -s {self.adbDevice} push {fromPath} {savePath}'
            print(adbCmd)
            return self.run_command(adbCmd)
        else:
            return []

    def isOptionRunning(self):
        isRun = (self.optionThread != None)
        print("R" if isRun else "r",end="",flush=True)
        return isRun
    
    
    def __async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
        
    def __stop_thread(self, thread):
        self.__async_raise(thread.ident, SystemExit)


    def stopOption(self):
        try:
            if self.optionThread:
                self.optionThread.terminate()
                self.optionThread = None
                return True
        except BaseException:
            pass
        finally:
            self.optionThread = None
            print("S")
            if self.option:
                self.option.stopLoopCheck()
            self.initOption()
        return False
    
    def initOption(self):
        print("initOption")
        self.option:OptionBU = None

    def isStartHideDevices(self):
        return config.isStartHideDevices

    def asynLoopRunOption(self):
        print("A",end="",flush=True)
        if self.isStartHideDevices():
            self.hideWindow()
        self.optionThread = multiprocessing.Process(target=self.loopRunOption, name=f"asynLoopRunOption_{self.pid}")
        # self.optionThread.setDaemon(True)
        self.optionThread.start()


    def loopRunOption(self):
        try:
            startTime = time.time()
            for i in range(config.startInterval):
                for tt in range(8):
                    time.sleep(1)
                if time.time() - startTime > (config.startInterval>>1):
                    # 一直没有拿到adb应该是启动出问题了。
                    rchoice = random.choice(["a","b"])
                    if rchoice == "a":
                        self.stop()
                    return
                self.refreshState()
                if self.adbDevice:
                    break
                print("W",end="",flush=True)
            if self.adbDevice:
                print("C",end="",flush=True)
                if self.option.bindAdbDevice(self.adbDevice).connect():
                    print("L",end="",flush=True)
                    self.option.loopCheck()
        except BaseException:
            import traceback
            traceback.print_exc()
            print("B",end="",flush=True)
        finally:
            self.stopOption()
            

    def sortwin(self):
        """ 需要打开多开器 """
        if self.memucCMD("sortwin", "SUCCESS: sort win finished."):
            return True
        return False
    
    def randomize(self):
        return self.memucCMD(f'randomize {self.cmd_i_n}', "SUCCESS: change device attributes finished.", timeOut=20)

    def asyncRename(self, newTitle):
        """ 虚拟机重命名 """
        def onStartReturn(res):
            if res:
                self.refreshState()
                self.saveCache()
        
        self.memucCMD(f'rename {self.cmd_i_n} {newTitle}', "SUCCESS: rename vm finished", timeOut=20, asynCallBack=onStartReturn)

    def rename(self, newTitle):
        """ 虚拟机重命名 """
        return self.memucCMD(f'rename {self.cmd_i_n} {newTitle}', "SUCCESS: rename vm finished", timeOut=20)
    
    def remove(self):
        self.memucCMD(f'remove {self.cmd_i_n}')

    def stop(self, saveCache=False):
        """ 结束 """
        def onStartReturn(res):
            if saveCache:
                self.refreshState()
                self.saveCache()
        
        self.memucCMD(f'stop {self.cmd_i_n}', "SUCCESS: stop vm finished.", timeOut=240, asynCallBack=onStartReturn)
        if saveCache:
            self.updateFinishTimes()
            self.saveCache()

        self.stopOption()
        self.optionThread = None


    def refreshState(self):
        """ 刷新模似器状态 """
        time.sleep(1)
        try:
            res = self.memucCMD(f'listvms {self.cmd_i_n}',timeOut=10)
            for r in res:
                rs = r.split(",")
                self.update(*rs)
            res = self.memucCMD(f'{self.cmd_i_n} adb version',timeOut=10)
            for r in res:
                if r.startswith("already connected to "):
                    self.adbDevice = r[len("already connected to "):].replace("\n","")
                    break
                elif "connect to" in r.split("\n")[0]:
                    try:
                        self.adbDevice = r.split("\n")[0].split("connect to ")[1]
                        os.system(f"adb -s {self.adbDevice} reconnect offline")
                    except BaseException:
                        return False
                    break
            if self.num != None and len(self.num) > 0:
                self.saveCache()
        except BaseException:
            print("Error refreshState!")
            return False
        return True

    def isRunEnough(self):
        """ 是否已经开很久机了 """
        if self.isRunning != "1":
            return False
        return self.isRunTooLong()

    def isRunTooLong(self, maxTime=None):
        """ 是否跑太久了 """
        oC = config.optionTimesConfig.get(self.option.signKey)
        hasRunTime = self.getHasRuntime()
        if maxTime == None:
            if oC:
                maxTime = oC.get("perTime",7200)
            else:
                maxTime = 7200
        if hasRunTime:
            if time.time()-hasRunTime > maxTime:
                return True
        return False
            
    def getHasRuntime(self):
        cs = psutil.process_iter()
        for c in cs:
            if str(c.pid) == str(self.pid):
                return c.create_time()
        return None
        

    def importMemu(self):
        """ 导入一个模拟器 """
        res = self.memucCMD(f'import "{config.MEmu_PATH}\\newM.ova"')
        print(res)
