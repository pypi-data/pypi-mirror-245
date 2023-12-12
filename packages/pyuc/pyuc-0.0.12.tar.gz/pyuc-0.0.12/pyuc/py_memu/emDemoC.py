import pyuc
from pyuc.py_memu.memuCU import MEmuCU
from .emDemoOption import EmDemoOption

class EmDemoC(MEmuCU):

    
    def initOption(self):
        self.option: EmDemoOption = EmDemoOption(self)

    