import pyuc
from pyuc.py_memu.memuCMU import MEmuCMU
from .emDemoC import EmDemoC


class EmDemoCM(MEmuCMU):

    def __init__(self):
        super().__init__()
        self.typeSign = None

    def createMEmuc(self):
        return EmDemoC()

    def fixSomeThs(self, dvs):
        for dv in dvs:
            d:EmDemoC = dvs[dv]
            if d.isRunEnough():
                self.asyncMemuStop(d)
        return False
        