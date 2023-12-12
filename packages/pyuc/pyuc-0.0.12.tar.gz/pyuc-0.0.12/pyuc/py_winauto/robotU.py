# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import os
if PyApiB.tryImportModule("pywinauto", installName="pywinauto"):
    import pywinauto
    from pywinauto.application import Application
    # https://github.com/blackrosezy/gui-inspect-tool


class RobotU(PyApiB):
    """
    windows界面操作机器人相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def dlGuiTool(self, savePath=None):
        """ 下载windows相关gui分析工具简化版 """
        if savePath == None:
            savePath = "./GuiTool.zip"
        pyuc.httpU().get("https://github.com/blackrosezy/gui-inspect-tool/archive/refs/heads/master.zip",savePath=savePath)


    @property
    def _application(self) -> pywinauto.application.Application:
        __app = getattr(self, "__application", None)
        if __app == None:
            __app = pywinauto.application.Application(backend="uia")
            setattr(self,"__application", __app)
        return __app
    
    @property
    def app(self) -> pywinauto.application.Application:
        __app = getattr(self, "__app", None)
        if __app:
            return __app
        __appPath = getattr(self, "__appPath", None)
        if not __appPath:
            raise RuntimeError("请先调用bindApp方法，设置应用路径。")
        appName = os.path.basename(__appPath)
        if self.is_process_running(appName):
            __app = self._application.connect(path=__appPath)
        else:
            __app = self._application.start(cmd_line=__appPath)
        setattr(self, "__app", __app)
        return __app
        

    def bindApp(self, appPath):
        """ 绑定应用，如果应用没有启动先启动，如果已经启动，直接连接上去。 """
        setattr(self, "__appPath", appPath)
        

    def is_process_running(self, process_name):
        for line in os.popen('tasklist'):
            if process_name in line:
                return True
        return False

    def screenShot(self, savePath):
        self.app.top_window().capture_as_image().save(savePath)
        