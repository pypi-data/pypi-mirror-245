# -*- coding: UTF-8 -*-
import pyuc
from pyuc.py_api_b import PyApiB
import os
if PyApiB.tryImportModule("mitmproxy", installName="mitmproxy==8.0.0,Werkzeug==2.2.2"):
    import mitmproxy
    from mitmproxy import proxy, options
    from mitmproxy.tools.dump import DumpMaster
    from mitmproxy.addons import core


class MitmproxyU(PyApiB):
    """
    中间人代理相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def request(self, flow: mitmproxy.http.HTTPFlow):
        pass

    def start(self, host, port):
        pass

    def installCertInAndroid(self,deviceName=None):
        self.setToThisProxyInAndroid()
        pyuc.adbU().shell("am start -a android.intent.action.VIEW -d http://mitm.it",serial=deviceName)

    def setToThisProxyInAndroid(self,deviceName=None):
        pyuc.adbU().shell(f"settings put global http_proxy {pyuc.envU().getLocalIp()}:8080",serial=deviceName)

    def delThisProxyInAndroid(self,deviceName=None, isReboot=False):
        if isReboot:
            pyuc.adbU().shell(f"settings delete global http_proxy",serial=deviceName)
            pyuc.adbU().shell(f"settings delete global global_http_proxy_host",serial=deviceName)
            pyuc.adbU().shell(f"settings delete global global_http_proxy_port",serial=deviceName)
            pyuc.cmdU().run(f"adb {f'-s {deviceName} ' if deviceName else ' '}reboot")
            # adb reboot
        else:
            pyuc.adbU().shell(f"settings put global http_proxy :0",serial=deviceName)
