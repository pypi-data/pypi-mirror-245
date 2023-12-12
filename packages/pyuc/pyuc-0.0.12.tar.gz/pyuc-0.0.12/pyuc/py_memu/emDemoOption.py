import pyuc
from pyuc.py_memu.optionBU import OptionBU
from pyuc.py_memu.memuCU import MEmuCU


class EmDemoOption(OptionBU):

    def __init__(self, mEmuC:MEmuCU):
        super().__init__(mEmuC)
        self.appName = "打开的应用名称"
        self.appIconPoint = (0,0)

    def on_xxxx(self, isDumpErr=False):
        """ 当前界面在xxxx时，会调用此方法 """
        pass

    def onNormalActivity(self, topAName, isDumpErr=False):
        return super().onNormalActivity(topAName, isDumpErr)

    def firstDoNormalOptions(self):
        return super().firstDoNormalOptions()
    