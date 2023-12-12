# -*- coding: utf-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import inspect, time, os, re
import multiprocessing
if PyApiB.tryImportModule("com.dtmilano.android",installName="androidviewclient"):
    from com.dtmilano.android.viewclient import ViewClient
    from com.dtmilano.android.adb.adbclient import Device


class OptionBU(PyApiB):

    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self,mEmuC):
        from .memuCU import MEmuCU
        self.signKey = None
        self.adbDevice = None
        self.mEmuC:MEmuCU = mEmuC
        self.device = None
        self.serialno = None
        self.__canLoopCheck = multiprocessing.Value('i',1)
        self.preActivity = None
        self.preTopAName = None
        self._needNextDump = True

    @property
    def canLoopCheck(self):
        """ 是否读完了 """
        return self.__canLoopCheck.value == 1


    @canLoopCheck.setter
    def canLoopCheck(self, value):
        self.__canLoopCheck.value = (1 if value else 0)

    def touchAppIcon(self, appName, appIconPoint=None):
        """ 打开应用，appName为应用名称，如果读不到会直接点击appIconPoint这个坐标点 """
        a = self.vc.findViewWithText(appName)
        if a:
            self.touch(a)
        elif appIconPoint and appIconPoint[0] > 0 and appIconPoint[1] > 0:
            self.tap(x=appIconPoint[0],y=appIconPoint[1])

    def on_Launcher(self, isDumpErr=False):
        """ 桌面 """
        self.touchAppIcon(appName=self.appName, appIconPoint=(0,0))

    def bindAdbDevice(self, adbDevice):
        """绑定adb设备 """
        self.adbDevice = adbDevice
        return self
    
    def isDeviceRunning(self, isRefresh=False):
        if isRefresh:
            self.mEmuC.refreshState()
        return self.mEmuC.isRunning == "1"
        
        
    def connect(self, retryTimes=20):
        """ 连接 """
        try:
            if not self.canLoopCheck:
                return False
            self.device, self.serialno = ViewClient.connectToDeviceOrExit(serialno=self.adbDevice, timeout=30)
            self.vc = ViewClient(self.device, self.serialno, autodump=False)
            print(self.serialno,"topActivity",self.device.getTopActivityName())
            return True
        except BaseException:
            print("Connect Exception!", self.mEmuC.num,",self.adbDevice=",self.adbDevice,",retryTimes=",retryTimes)
            # import traceback
            # traceback.print_exc()
            if self.mEmuC.isRunning == "1":
                if retryTimes >= 0:
                    os.system(f"adb -s {self.adbDevice} reconnect offline")
                    for ii in range(20):
                        time.sleep(1)
                    return self.connect(retryTimes-1)
                else:
                    self.mEmuC.stop()
            return False

    
    def dump(self,retryTimes=0):
        hasDump = False
        try:
            self.vc.dump()
            hasDump = True
        except BaseException:
            # import traceback
            # traceback.print_exc()
            hasDump = False
        finally:
            if retryTimes > 0:
                time.sleep(1)
                return self.dump(retryTimes-1)
            print("*" if hasDump else "X",end="",flush=True)
            return hasDump
        
    def fixDumpErr(self, topAName=None):
        print("fixDumpErr!", self.mEmuC.num, self.mEmuC.adbDevice, topAName)
        

    def getAllTexts(self):
        """ 获取当前界面的所有文本 """
        vvv = self.vc.findViewsWithAttributeThatMatches("text",re.compile("\S"))
        return list(map(lambda x:x.getText(),vvv))

    def onDumpErr(self, topAName):
        res = False
        methodNames = dir(self)
        hasRunActivityFun = False
        for mN in methodNames:
            if self._needNextDump:
                break
            methodName, activityName = None, None
            if topAName and mN.startswith("on_"):
                onActivityName = mN[3:]
                if topAName.endswith(onActivityName):
                    methodName = mN
                    activityName = onActivityName
            if methodName:
                try:
                    checkMethod = getattr(self, methodName)
                    if checkMethod and self.canLoopCheck and callable(checkMethod):
                        if checkMethod(True):
                            res = True
                except BaseException:
                    import traceback
                    traceback.print_exc()
                if activityName:
                    hasRunActivityFun = True
                if not hasRunActivityFun:
                    self.onNormalActivity(topAName, True)
        self.preTopAName = topAName
        if topAName:
            self.preActivity = topAName.split(".")[-1]
        else:
            self.preActivity = None
        return res
    
    def onNormalActivity(self, topAName, isDumpErr=False):
        """ 除了已定义的on_[activityName]外的其它界面，就会回调此方法 """
        return False

    def stopLoopCheck(self):
        self.canLoopCheck = False

    def firstDoNormalOptions(self):
        """ 所有on_xxxx方法之前会调用此方法 """
        pass
        
    def loopCheck(self):
        setattr(self, "__loopChecking", True)
        try:
            dumpErr = 0
            topANameNoneTimes = 0
            while self.mEmuC and self.isDeviceRunning(isRefresh=False):
                if not self.canLoopCheck:
                    break
                self._needNextDump = False
                for _ in range(3):
                    time.sleep(1)
                topAName = None
                try:
                    topAName = self.device.getTopActivityName()
                    # print(topAName)
                except BaseException:
                    pass
                dumpRes = self.dump()
                if not self.canLoopCheck:
                    break
                if (not dumpRes):
                    if not self.isDeviceRunning(isRefresh=True):
                        # 设备关了
                        break
                    if topAName == None:
                        topANameNoneTimes += 1
                        if topANameNoneTimes > 20:
                            # 应该是出问题了，直接关掉重启
                            topANameNoneTimes = 0
                            self.mEmuC.stop()
                            continue
                    else:
                        topANameNoneTimes = 0
                        if self.onDumpErr(topAName):
                            # onDumpErr处理好了，无需走fixDumpErr的流程
                            continue
                    dumpErr += 1
                    if dumpErr > 4:
                        dumpErr = 0
                        self.fixDumpErr(topAName)
                    continue
                if not self.canLoopCheck:
                    break
                try:
                    self.firstDoNormalOptions()
                except BaseException:
                    import traceback
                    traceback.print_exc()
                if not self.canLoopCheck:
                    break
                methodNames = dir(self)
                hasRunActivityFun = False
                for mN in methodNames:
                    if self._needNextDump:
                        break
                    if not self.canLoopCheck:
                        break
                    methodName, activityName = None, None
                    if mN.startswith("do"):
                        methodName = mN
                    elif topAName and mN.startswith("on_"):
                        onActivityName = mN[3:]
                        if topAName.endswith(onActivityName):
                            methodName = mN
                            activityName = onActivityName
                    if methodName:
                        try:
                            checkMethod = getattr(self, methodName)
                            if checkMethod and callable(checkMethod):
                                checkMethod()
                        except BaseException:
                            import traceback
                            traceback.print_exc()
                        if activityName:
                            hasRunActivityFun = True
                if not self.canLoopCheck:
                    break
                if not hasRunActivityFun:
                    self.onNormalActivity(topAName)
                self.preTopAName = topAName
                if topAName:
                    self.preActivity = topAName.split(".")[-1]
                else:
                    self.preActivity = None
        except BaseException:
            import traceback
            traceback.print_exc()
        finally:
            self.stopLoopCheck()
            setattr(self, "__loopChecking", False)

    def tap(self, x, y):
        self.mEmuC.adbShell(f"input tap {x} {y}") 

    def inputText(self, text):
        self.mEmuC.memucCMD(f'input -i {self.mEmuC.num} "{text}"')
        self.mEmuC.adbShell(f"input text {text}") 

    def rollball(self):
        self.vc.swipe(startX=367,startY=1127,endX=488,endY=311,steps=1000)
        # self.mEmuC.adbShell(f"input trackball roll") 

    def keyevent(self, keyCode):
        self.mEmuC.adbShell(f"input keyevent {keyCode}")  

    def isaudioPlaying(self):
        res = self.mEmuC.isaudioPlaying()
        # print(self.mEmuC.num,":P:",res)
        return res

    def playOrStart(self):
        self.keyevent(126)

    def playOrPause(self):
        self.keyevent(85)


    def goBackKey(self):
        self.keyevent(4)
        self.waitNextDump()


    def waitNextDump(self):
        self._needNextDump = True


    def touch(self, view):
        if view and view.getVisibility():
            view.touch()
            print(view.getText())


    
    def findViewWithText(self, text, parentClassName=None,isSingle=True):
        if self.vc:
            if parentClassName or not isSingle:
                views = self.findViewsWithAttribute("text",text)
                _views = []
                if views:
                    for view in views:
                        if self.isParentClass(view, parentClassName,isNoneTrue=True):
                            if isSingle:
                                return view
                            else:
                                _views.append(view)
                return _views
            else:
                return self.vc.findViewWithText(text)
        return None


    def isParentClass(self, view, className, isNoneTrue=False):
        if isNoneTrue and className == None:
            return True
        return view.parent.getClass() == className
    
    
    def findViewsWithAttribute(self,attr,val,root: str ="ROOT"):
        if not self.vc:
            return []
        return self.vc.findViewsWithAttribute(attr,val,root)
    
