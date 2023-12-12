

def printHelp():
    print(' pyuts.py_crawl')
    print('example: python -m pyuc.py_memu -i projectName')

def initProject(projectName):
    import pyuc
    pyutsPath = pyuc.__file__[:-12]
    copyName = projectName
    if '/' in projectName:
        names = projectName.split('/')
        projectName = names[-1]
    # copy emDemoC.py
    settingStr = pyuc.fileU().read_str(f'{pyutsPath}/py_memu/emDemoC.py')
    settingStr = settingStr.replace('emDemo', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('EmDemo', f"{projectName[:1].upper()}{projectName[1:]}")
    pyuc.fileU().write_str(f"./{projectName}C.py", settingStr)
    # copy emDemoOption.py
    settingStr = pyuc.fileU().read_str(f'{pyutsPath}/py_memu/emDemoOption.py')
    settingStr = settingStr.replace('emDemo', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('EmDemo', f"{projectName[:1].upper()}{projectName[1:]}")
    pyuc.fileU().write_str(f"./{projectName}Option.py", settingStr)
    # copy emDemoCM.py
    settingStr = pyuc.fileU().read_str(f'{pyutsPath}/py_memu/emDemoCM.py')
    settingStr = settingStr.replace('emDemo', f"{projectName[:1].lower()}{projectName[1:]}")
    settingStr = settingStr.replace('EmDemo', f"{projectName[:1].upper()}{projectName[1:]}")
    pyuc.fileU().write_str(f"./{projectName}CM.py", settingStr)
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) <= 2:
        printHelp()
        exit()
    else:
        action = sys.argv[1]
        if action in ['--init',"-i","-I"]:
            # 创建工程
            projectName = sys.argv[2]
            initProject(projectName)
