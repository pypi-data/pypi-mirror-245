# -*- coding: UTF-8 -*-
import importlib, subprocess


class PyApiB:
    """
    所有需要对外提供的类，都需要承继此类
    """
    instances = {}

    @staticmethod
    def _produce(key, cls):
        _signKey = "default"
        if key:
            _signKey = key
        newKey = f"{cls.__name__}_{_signKey}"
        if newKey not in PyApiB.instances:
            PyApiB.instances[newKey] = cls()
        v:cls = PyApiB.instances[newKey]
        setattr(v,"__signKey__", _signKey)
        return v
    
    @property
    def _signKey(self):
        return getattr(self, "__signKey__", None)

    @staticmethod
    def tryImportModule(moduleName:str, installName:str=None, source="https://mirrors.aliyun.com/pypi/simple/"):
        if installName == None:
            installName = moduleName
        try:
            importlib.import_module(moduleName)
        except ImportError:
            installNames = [installName]
            if "," in installName:
                installNames = installName.split(",")
            if source:
                args = ["pip", "install",
                        "-i", source,
                        *installNames]
            else:
                args = ["pip", "install",
                        # "-i", source,
                        *installNames]
            try:
                subprocess.check_call(args)
                print(f"pip install Successfull! ModuleName=[{installName}]")
                return True
            except subprocess.CalledProcessError:
                print(f"pip install ERROR! ModuleName=[{installName}]")
                return False
        return True


    def __init__(self):
        pass
