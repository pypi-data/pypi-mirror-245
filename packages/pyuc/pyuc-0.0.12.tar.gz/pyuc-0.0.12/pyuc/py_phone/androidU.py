# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
from pyuc.py_recg.imgU import ImgU
if PyApiB.tryImportModule("uiautomator2",installName="uiautomator2"):
    import uiautomator2 as u2
    from uiautomator2 import Device, UiObject
    # pip install weditor==0.5.3
if PyApiB.tryImportModule("weditor", installName="weditor==0.5.3"):
    from weditor.__main__ import main as weditorRun

# https://www.cnblogs.com/thyuan/p/14907213.html


class AndroidXpathNode:
    # https://blog.csdn.net/weixin_39561577/article/details/111062680
    # https://zhuanlan.zhihu.com/p/599176415?utm_id=0

    def __init__(self, d:Device, xpath:str=None, node:u2.xpath.XPathSelector=None, ele:u2.xpath.XMLElement=None):
        self.d = d
        self.__node:u2.xpath.XPathSelector = node
        self.__ele:u2.xpath.XMLElement=ele
        self.__xpath = xpath

    @property
    def info(self)->dict:
        if self.ele == None:
            return {}
        else:
            return self.ele.info
    
    @property
    def exists(self):
        return self.ele != None
        
    @property
    def node(self)->u2.xpath.XPathSelector:
        if self.__node == None and self.__xpath != None:
            self.__node = self.d.xpath(self.__xpath)
        if self.__node == None and self.__ele != None:
            self.__node = self.d.xpath(self.__ele.get_xpath())
        return self.__node
    
    @property
    def ele(self)->u2.xpath.XMLElement:
        if self.__ele == None:
            if not self.node:
                self.__ele = None
            else:
                self.__ele = self.node.match()
        return self.__ele

    @property
    def xpath(self)->str:
        if not self.__xpath or ("@" in self.__xpath):
            if not self.ele:
                self.__xpath = None
            else:
                self.__xpath = self.ele.get_xpath()
        return self.__xpath
    
    def findByXpath(self, xpath:str):
        """ 在当前节点查找元素 """
        return AndroidXpathNode(self.d, xpath=None if not self.xpath else (self.xpath+xpath))

    def child(self, className=None, attrKey:str=None, attrValue:str=None, findType:str=None, index:int=None):
        classStr = "" if className == None else className
        attrStr = f'[{AndroidXpathNode.XPATH_attr(attrKey, attrValue, findType)}]' if attrKey and attrValue else ""
        indexStr = ""
        if index != None:
            if index < 0:
                indexStr = f'[last(){str(index+1) if index < -1 else ""}]'
            elif index > 1:
                indexStr = f'[{index}]'
        attrStrs = f"{attrStr}{classStr}{indexStr}"
        if not attrStr and not classStr and not indexStr:
            attrStrs = "*"
        return AndroidXpathNode(self.d, xpath=None if not self.xpath else (self.xpath+f'/{attrStrs}'))

    def parent(self):
        return AndroidXpathNode(self.d, xpath=None if not self.xpath else self.xpath[:-len(self.xpath.split("/")[-1])-1])
        
    def children(self):
        nos:list[AndroidXpathNode] = []
        if self.xpath:
            for ele in self.d.xpath(self.xpath+"/*").all():
                nos.append(AndroidXpathNode(self.d, ele=ele))
        return nos

    def nextBrother(self):
        """ 下一个兄弟元素 """
        return AndroidXpathNode(self.d, xpath=None if not self.xpath else (self.xpath+"/following-sibling::*"))
    
    def preBrother(self):
        """ 上一个兄弟元素 """
        return AndroidXpathNode(self.d, xpath=None if not self.xpath else (self.xpath+"/following::*"))

    @staticmethod
    def XPATH_attr(attrKey:str, attrValue:str, findType:str=None):
        """ 
        返回查找元素属性的xpath方法
        attrKey  属性键，像text, content-desc, resource-id
        attrValue 为文本内容 \n
        findType : str|None  \n
                   "match"表示用正则语句进行模糊查找；\n
                   "contain"表示文本中完含text文本；\n
                   "startwith"表示以text文本开头\n
        例如：正则表达式 或是 全符合
        f'[{AndroidXpathNode.XPATH_attr("text", "*xxx", "match")} or {AndroidXpathNode.XPATH_attr("content-desc", "xxx2")}]' 
        """
        if findType == "match":
            return f're:match(@{attrKey},"^{attrValue}")'
        elif findType == "contain":
            return f'contains(@{attrKey},"{attrValue}")'
        elif findType == "startwith":
            return f'starts-with(@{attrKey},"{attrValue}")'
        else:
            return f'@{attrKey}="{attrValue}"'

    # def click(self):
    #     self.node.click
    


class AndroidU(PyApiB):
    """
    Android自动化相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    @property
    def serial(self):
        __serial = getattr(self, "__serial", None)
        if __serial == None:
            if self._signKey != "default":
                __serial = self._signKey
            setattr(self, "__serial", __serial)
        return __serial

    @property
    def d(self)->Device:
        __device = getattr(self, "__device", None)
        if __device == None:
            __device = u2.connect(self.serial)
            setattr(self, "__device", __device)
        return __device

    def runDebug(self):
        """ 启动调试后台 """
        weditorRun()

    def healthCheck(self):
        """ 检查并维持设备端守护进程处于运行状态 """
        self.d.healthcheck()

    def appInstall(self, url):
        """ 安装应用，从URL安装 """
        self.d.app_install(url)

    def appUninstall(self, packageName):
        """ 卸载应用 """
        return self.d.app_uninstall(packageName)

    def appStart(self, packageName, activity=None, waitStarted=False, stopIfOn=False):
        """ 启动应用 """
        self.d.app_start(package_name=packageName, activity=activity,wait=waitStarted, stop=stopIfOn)

    def appStop(self, packageName):
        """ 停止应用 """
        self.d.app_stop(packageName)

    def appClear(self, packageName):
        """ 清空应用数据 """
        self.d.app_clear(packageName)

    def appStopAll(self, excludes:list=[]):
        """ 停止所有应用，除了excludes里面的包名 """
        return self.d.app_stop_all(excludes)

    def appInfo(self, packageName):
        """ 获取应用信息 """
        return self.d.app_info(packageName=packageName)

    def appIcon(self, packageName)->ImgU:
        """ 获取应用图标 """
        img = self.d.app_icon(packageName=packageName)
        return ImgU().initImg(img)

    def push(self, src, dst, mode:int=0o777,showProgress=False):
        """ 推scr的文件到手机中dst路径上 """
        return self.d.push(src, dst, mode, showProgress)
    
    def pull(self, src, dst):
        """ 将手机中scr的文件拉到电脑中dst路径上 """
        return self.d.pull(src, dst)
    
    def screenOn(self):
        self.d.screen_on()

    def screenOff(self):
        self.d.screen_off()

    @property
    def isScreenOn(self):
        """ 屏幕是否为亮屏 """
        return self.d.info.get("screenOn")

    def press(self, key, meta=None):
        """ 
        按下按键key：\n
        "home": 主页\n
        "back": 返回\n
        "left": 左\n
        "right": 右\n
        "up": 上\n
        "down": 下\n
        "center": 选中\n
        "menu": 菜单\n
        "search": 搜索\n
        "enter": 回车\n
        "delete": 删除\n
        "rencent": 近期活动\n
        "volume_up": 音量+\n
        "volume_down": 音量-\n
        "volume_mute": 音量静音\n
        "camera": 相机\n
        "power": 电源\n
        """
        return self.d.press(key=key,meta=meta)

    def unlock(self):
        """ 解锁屏幕 """
        return self.d.unlock()
    
    def click(self, x, y):
        """ 点击 \n
        注意：x和y为int时，表示点击像素坐标;\n当为float时，像x=0.5,y=0.5时，则表示屏幕正中间\n 
        """
        return self.d.click(x, y)

    def doubleClick(self, x, y, duration:float=0.1):
        """ 双击\n
        注意：x和y为int时，表示点击像素坐标;\n当为float时，像x=0.5,y=0.5时，则表示屏幕正中间\n 
         """
        return self.d.double_click(x, y, duration=duration)

    def longClick(self, x, y, duration:float=0.5):
        """ 长按\n
        注意：x和y为int时，表示点击像素坐标;\n当为float时，像x=0.5,y=0.5时，则表示屏幕正中间\n 
         """
        return self.d.long_click(x, y, duration=duration)

    def swipe(self, sx, sy, ex, ey, duration:float=0.5):
        """ 滑动\n
        注意：x和y为int时，表示点击像素坐标;\n当为float时，像x=0.5,y=0.5时，则表示屏幕正中间\n 
         """
        return self.d.swipe(sx, sy, ex, ey, duration=duration)
    
    def swipe_points(self, points, duration:float=0.5):
        """ 多点滑动，可以用于解锁九宫格的功能 """
        return self.d.swipe_points(points, duration=duration)
    
    def drag(self, sx, sy, ex, ey, duration:float=0.5):
        """ 拖动\n
        注意：x和y为int时，表示点击像素坐标;\n当为float时，像x=0.5,y=0.5时，则表示屏幕正中间\n 
         """
        return self.d.drag(sx, sy, ex, ey, duration=duration)
    
    @property
    def orientation(self):
        """ 
        获取手机方向
        left/l: rotation=90 , displayRotation=1
        right/r: rotation=270, displayRotation=3
        natural/n: rotation=0 , displayRotation=0
        upsidedown/u: rotation=180, displayRotation=2
        """
        return self.d.orientation


    def setOrientation(self, value):
        """ 
        设置手机方向。例如：value="r" 表示设置方向为向右
        left/l: rotation=90 , displayRotation=1
        right/r: rotation=270, displayRotation=3
        natural/n: rotation=0 , displayRotation=0
        upsidedown/u: rotation=180, displayRotation=2
        """
        self.d.set_orientation(value)

    def freezeRotation(self, freezed=True):
        """ 冻结 or 开启 旋转。 freezed为True时不可以旋转，反之为可以旋转 """
        self.d.freeze_rotation(freezed=freezed)

    @property
    def screenShot(self)->ImgU:
        """ 当前截图，返回ImgU格式 """
        return ImgU().initImg(self.d.screenshot())
    
    def dump(self,isCompress=False, toXML=False):
        """
        转储UI层次结构
        效果等同于 "adb shell uiautomator dump"
        isCompress:是否压缩
        toXML (bool): 是否format xml
        """
        return self.d.dump_hierarchy(compressed=isCompress, pretty=toXML)

    def openNotification(self):
        """ 下拉打开通知栏 """
        return self.d.open_notification()
    
    def openQuickSettings(self):
        """ 下拉打开快速设置 """
        return self.d.open_quick_settings()
    
    def openIdentify(self, theme="black"):
        """ 开启主题模式，theme为black时表示暗黑模式，red表示解除暗黑模式 """
        self.d.open_identify(theme)
        

    def findByAttr(self, attrKey, attrValue, findType=None)->AndroidXpathNode:
        """ 
        找出所有元素中符合attrKey为attrValue的元素 \n
        attrKey  属性键，像text, content-desc, resource-id
        attrValue 为文本内容 \n
        findType : str|None  \n
                   "match"表示用正则语句进行模糊查找；\n
                   "contain"表示文本中完含text文本；\n
                   "startwith"表示以text文本开头\n
        """
        return AndroidXpathNode(self.d, xpath=f'//*[{AndroidXpathNode.XPATH_attr(attrKey, attrValue, findType)}]')

    def saveDump(self,savePath=None):
        pyuc.fileU().write_str(savePath, self.dump())