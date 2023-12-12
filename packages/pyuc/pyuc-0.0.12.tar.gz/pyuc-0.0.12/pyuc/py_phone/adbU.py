# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import time
import re
if PyApiB.tryImportModule("adbutils",installName="adbutils"):
    from adbutils import adb,AdbDevice
if PyApiB.tryImportModule("com.dtmilano.android",installName="androidviewclient"):
    from com.dtmilano.android.viewclient import ViewClient
    from com.dtmilano.android.adb.adbclient import Device


class AdbU(PyApiB):
    """
    adb相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self):
        self.asyncU = pyuc.asyncU()
        self.__devices = {}

    def devices(self):
        """ 获取所有可用的设备 """
        return adb.devices()

    @property
    def serial(self):
        __serial = getattr(self, "__serial", None)
        if __serial == None:
            if self._signKey != "default":
                __serial = self._signKey
            setattr(self, "__serial", __serial)
        return __serial

    def device(self)->AdbDevice:
        """ 获取设备,当只有一个设备时，可以不填serial """
        d = self.__devices.get(str(self.serial))
        if d == None:
            d = adb.device(self.serial)
            self.__devices[str(self.serial)] = d
        return self.__devices[str(self.serial)]

    def screenshot(self, savePath='screen.jpg'):
        try:
            d = self.device()
            remote_tmp_path = "/data/local/tmp/screenshot.png"
            d.shell(["rm", remote_tmp_path])
            d.shell(["screencap", "-p", remote_tmp_path])
            d.sync.pull(remote_tmp_path, savePath)
        except BaseException:
            return False
        return True

    def click(self, x, y, times=1):
        if times <= 0:
            return
        elif times == 1:
            d = self.device()
            d.click(x, y)
        else:
            self.asyncU.asyncRun(target=self.click,args=(x,y,times-1))
            time.sleep(0.2)
            
    def shell(self, cmdLine):
        d = self.device()
        return d.shell(cmdLine.split(" "))
        
    def swipe(self, x1, y1, x2, y2, ss):
        """ swipe from(10, 10) to(200, 200) 0.5s """
        d = self.device()
        d.swipe(x1, y1, x2, y2, ss)
        
    def window_size(self):
        d = self.device()
        return d.window_size()
    
    def rotation(self):
        d = self.device()
        return d.rotation()
    
    def keyHome(self):
        self.keyEvent("HOME")
    
    def keyBack(self):
        self.keyEvent("BACK")
        
    def keyEvent(self, keyEvent):
        d = self.device()
        d.keyevent(keyEvent)
        
    def send_keys(self, keys):
        d = self.device()
        d.send_keys(keys)
        
    def is_screen_on(self):
        d = self.device()
        d.is_screen_on()
        
    def open_browser(self, url):
        d = self.device()
        d.open_browser(url)
        
    def startScreenRecord(self):
        """ 开始录屏并返回一个句柄 """
        d = self.device()
        r = d.screenrecord(no_autostart=True)
        r.start()
        return r
        
    def stopScreenRecord(self, startRecordH, savePath='./video.mp4'):
        """ 停止录屏,startRecordH为录屏句柄 """
        startRecordH.stop_and_pull(savePath)
    
    @property
    def viewClient(self)->ViewClient:
        vc = getattr(self, "__viewClient", None)
        if vc == None:
            try:
                device, self.serialno = ViewClient.connectToDeviceOrExit(serialno=self.serial, timeout=30)
                vc = ViewClient(device, self.serialno, autodump=False)
                setattr(self, "__viewClient", vc)
            except BaseException:
                print("Connect Exception!", "self.serial=",self.serial)
        return vc

    def dump(self,window = -1,sleep=0,retryTimes=0):
        hasDump = False
        try:
            self.viewClient.dump(window=window, sleep=sleep)
            hasDump = True
        except BaseException:
            # import traceback
            # traceback.print_exc()
            hasDump = False
        finally:
            if retryTimes > 0:
                time.sleep(1)
                return self.dump(window, sleep, retryTimes-1)
            print("*" if hasDump else "X",end="",flush=True)
            return hasDump

        
    def getAllTexts(self):
        """ 获取当前界面的所有文本 """
        return list(map(lambda x:x.getText(),self.viewClient.findViewsWithAttributeThatMatches("text",re.compile("\S"))))

    def getWindowNames(self):
        """ 获取当前界面中存在的所有视图名称+ """
        res = self.shell("dumpsys window w")
        rss = res.split("\n")
        windowNames = []
        for rs in rss:
            if "Surface(name=" in rs:
                windowNames.append(rs.split("Surface(name=")[1].split(")")[0])
        return  windowNames
    
    def isCurrentActivityName(self, activityName):
        for rs in self.getWindowNames():
            if activityName in rs:
                return True
        return False

    def stopApp(self, packageName):
        self.shell(f"am force-stop {packageName}")

    def startApp(self, packageName, startActivityName):
        self.shell(f"am start -n {packageName}/{startActivityName}")

    def restartApp(self, packageName, startActiviyName):
        self.stopApp(packageName)
        self.startApp(packageName, startActiviyName)
    