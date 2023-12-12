# -*- coding: UTF-8 -*-
# pip install opencv-python
import pyuc
from pyuc.py_api_b import PyApiB
from PIL import Image,ImageFilter
from pyuc.py_recg.imgU import ImgU
import os
import bisect
if PyApiB.tryImportModule("aircv", installName="aircv"):
    import aircv as ac
if PyApiB.tryImportModule("cv2", installName="opencv-python"):
    import cv2
if PyApiB.tryImportModule("pytesseract", installName="pytesseract"):
    import pytesseract 
    # https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
    # tesseract --list-langs 
    # 训练下载：https://github.com/nguyenq/jTessBoxEditor/releases/tag/


class TesseractU(PyApiB):
    """
    文字识别相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)

    def __init__(self):
        super().__init__()
        self.trainFolderPath = "./TesseractTrainDataset"

    def image_to_num(self,imgU:ImgU, lang="eng", config="--psm 7 -c tessedit_char_whitelist=0123456789."):
        return pytesseract.image_to_string(imgU.getPilImg(),lang=lang,config=config)

    def setTrainFolderPath(self, trainFolderPath):
        self.trainFolderPath = trainFolderPath

    def pushToTrainFolder(self,  imgU:ImgU, preGrayFilt=250):
        """ 保存入训练目录 """
        imgU.gray(preGrayFilt).save(f"{self.trainFolderPath}/{imgU.randomPngName()}")
        

    # def mergeTrainFolderImage(self, savePath):
    #     files = os.listdir(self.trainFolderPath)
    #     # print(files)
    #     temps = {}
    #     charImgs = []
    #     for ff in files:
    #         imgU = pyuc.imgU().initImg(f'{self.trainFolderPath}/{ff}')
    #         contours = cv2.findContours(imgU.getNpImg(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    

    def image_to_num_by_folder(self, imgU:ImgU, folderPath:str, floadLen=1):
        """ 单行 floadLen:小数点后几位 """
        # https://zhuanlan.zhihu.com/p/365202405
        files = os.listdir(folderPath)
        
        # print(files)
        temps = {}
        for ff in files:
            temps[ff[:-4]] = cv2.imread(f'{folderPath}/{ff}', cv2.IMREAD_GRAYSCALE)

        charH,charW = 0,0
        for k in temps:
            cH,cW = temps[k].shape
            charH = max(charH, cH)+1
            charW = max(charW, cW)+1

        for k in temps:
            temps[k] = cv2.resize(temps[k],(charW, charH))
        # charH, charW = list(temps.values())[0].shape
        # charH, charW = 10, 6
        # print(charW, charH)

        contours = cv2.findContours(imgU.getNpImg(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        boundRects = list(map(lambda cnt:cv2.boundingRect(cnt),contours)) # [[x,y,w,h]]
        if not boundRects:
            return ""

        boundHs = list(map(lambda br:br[3], boundRects))
        boundWs = list(map(lambda br:br[2], boundRects))

        # boundHAVG = sum(boundHs)/len(boundHs)
        # mayHIndex = bisect.bisect_left(boundHs, boundHAVG)
        # # print("mayHIndex", mayHIndex)
        # mayBoundH = boundHs[mayHIndex]
        # mayBoundW = boundWs[mayHIndex]

        mayBoundH = max(boundHs)
        mayBoundW = max(boundWs)
        if mayBoundW < mayBoundH * (charW/charH) + 1:
            # 可能是全1
            mayBoundW = mayBoundH * (charW/charH)

        result = []
        for [x,y,w,h] in boundRects:
            # 按照高度筛选
            if mayBoundH+(mayBoundH>>1) > h > (mayBoundH>>1):
                result.append([x,y,w,h])

        result.sort(key=lambda x:x[0])
        if len(result) == 0:
            return ""
        # print(result)
        # 过滤和添加可能为空格或小数点的方格
        # result = [[3, 2, 5, 10], [9, 2, 6, 9], [16, 2, 6, 9], [23, 2, 6, 9],[29, 2, 6, 9], [35, 2, 6, 10]]
        newResult = [result[0]]
        for iii in range(1,len(result)):
            if result[iii][0]-result[iii-1][0] <= int(mayBoundW*0.25):
                # 矩离太近了不要了
                pass
            elif result[iii][0]-result[iii-1][0] <= int(mayBoundW*1.25):
                newResult.append(result[iii])
            else:
                # 间隔差多有一个字符宽了，应该是个.
                newResult.append([0,0,0,0])
                newResult.append(result[iii])
        result = newResult

        tttt = ""
        zzz = 0
        for x, y, w, h in result:    
            if x==0 and y==0 and w==0 and h==0:
                tttt += "."
                continue
            digit = cv2.resize(imgU.getNpImg()[y:y+h, x:x+w], (charW, charH))
            
            zzz+=1
            res = []
            for key in temps:
                # TODO 改为计算相同的数量比
                res.append((key, self.sim(digit, temps[key])))
            res.sort(key=lambda x:x[1])
            # print(res)
            # print(str(f"{res[-1][0]}"))
            tttt+=str(f"{res[-1][0]}")
        if tttt.count(".")>1:
            tttt = tttt[:-2].replace(".","") + tttt[-2:]
        if tttt.count(".")==1:
            if len(tttt)>floadLen+1 and tttt[-floadLen-1] != ".":
                tttt = tttt.replace(".","")
        if len(tttt)>2 and tttt[0] == "0":
            return "8"+tttt[1:]
            # return ""
        return tttt
    
    def maxSim(self, imgU:ImgU, folderPath:str):
        files = os.listdir(folderPath)
        sims = [0.0]
        for ff in files:
            if os.path.isdir(f'{folderPath}/{ff}'):
                sims.append(self.maxSim(imgU, f'{folderPath}/{ff}'))
            else:
                sims.append(self.sim(imgU.getNpImg(),ImgU().initImg(f'{folderPath}/{ff}').getNpImg()))
        return max(sims)
                

    
    def image_cut_num(self, imgU:ImgU, folderPath:str, minH=10, maxH=18, sim=0.8):
        contours = cv2.findContours(imgU.getNpImg(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        pyuc.fileU().mkdir(folderPath)
        boundRects = list(map(lambda cnt:cv2.boundingRect(cnt),contours)) # [[x,y,w,h]]
        if boundRects:
            for [x,y,w,h] in boundRects:
                if maxH > h > minH:
                    ii = imgU.crop((x,y, x+w, y+h))
                    if self.maxSim(ii, folderPath) < sim:
                        ii.save(f"{folderPath}/{imgU.randomPngName()}")

    def clear_image_cut_sim(self, folderPath:str, sim=0.8):
        files = os.listdir(folderPath)
        # print(files)
        temps = {}
        for ff in files:
            if os.path.isdir(f'{folderPath}/{ff}'):
                for f in os.listdir(f'{folderPath}/{ff}'):
                    temps[f"{ff}:{f[:-4]}"] = ImgU().initImg(f'{folderPath}/{ff}/{f}')
        delKeys = []
        keys = list(temps.keys())
        for i in range(len(keys)-1):
            for j in range(i+1, len(keys)):
                if self.sim(temps[keys[i]].getNpImg(),temps[keys[j]].getNpImg()) > sim:
                    delKeys.append(keys[i])
                    break
        for delKey in delKeys:
            print(f"Clear simImage:{delKey}")
            temps[delKey].remove()

    
    def image_to_num_by_folder2(self, imgU:ImgU, folderPath:str, floadLen=1):
        """ 单行 floadLen:小数点后几位 """
        # https://zhuanlan.zhihu.com/p/365202405
        files = os.listdir(folderPath)
        # print(files)
        temps = getattr(self, "__temp_num_source_", None)
        charH = getattr(self, "__temp_num_source_H", 0)
        charW = getattr(self, "__temp_num_source_W", 0)
        if not temps:
            temps = {}
            for ff in files:
                if os.path.isdir(f'{folderPath}/{ff}'):
                    for f in os.listdir(f'{folderPath}/{ff}'):
                        temps[f"{ff}:{f[:-4]}"] = cv2.imread(f'{folderPath}/{ff}/{f}', cv2.IMREAD_GRAYSCALE)
            for k in temps:
                cH,cW = temps[k].shape
                charH = max(charH, cH)+1
                charW = max(charW, cW)+1
            for k in temps:
                temps[k] = cv2.resize(temps[k],(charW, charH))

            setattr(self, "__temp_num_source_", temps)
            setattr(self, "__temp_num_source_H", charH)
            setattr(self, "__temp_num_source_W", charW)
        # charH, charW = list(temps.values())[0].shape
        # charH, charW = 10, 6
        # print(charW, charH)

        contours = cv2.findContours(imgU.getNpImg(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        boundRects = list(map(lambda cnt:cv2.boundingRect(cnt),contours)) # [[x,y,w,h]]
        if not boundRects:
            return ""

        boundHs = list(map(lambda br:br[3], boundRects))
        boundWs = list(map(lambda br:br[2], boundRects))

        # boundHAVG = sum(boundHs)/len(boundHs)
        # mayHIndex = bisect.bisect_left(boundHs, boundHAVG)
        # # print("mayHIndex", mayHIndex)
        # mayBoundH = boundHs[mayHIndex]
        # mayBoundW = boundWs[mayHIndex]
        mayBoundH = max(boundHs)
        mayBoundW = max(boundWs)
        if mayBoundW < mayBoundH * (charW/charH) + 1:
            # 可能是全1
            mayBoundW = mayBoundH * (charW/charH)
        if mayBoundW/mayBoundH > (charW/charH):
            # 估计有什么很长的东西
            mayBoundW = mayBoundH * (charW/charH)

        result = []
        for [x,y,w,h] in boundRects:
            # 按照高度筛选
            if mayBoundH+(mayBoundH>>1) > h > (mayBoundH>>1):
                result.append([x,y,w,h])

        result.sort(key=lambda x:x[0])
        if len(result) == 0:
            return ""
        # print(result)
        # 过滤和添加可能为空格或小数点的方格
        # result = [[3, 2, 5, 10], [9, 2, 6, 9], [16, 2, 6, 9], [23, 2, 6, 9],[29, 2, 6, 9], [35, 2, 6, 10]]
        newResult = [result[0]]
        for iii in range(1,len(result)):
            if result[iii][0]-result[iii-1][0] <= int(mayBoundW*0.2):
                # 矩离太近了不要了
                pass
            elif result[iii][0]-result[iii-1][0] <= int(mayBoundW*1.0):
                newResult.append(result[iii])
            else:
                # 间隔差多有一个字符宽了，应该是个.
                newResult.append([0,0,0,0])
                newResult.append(result[iii])
        result = newResult

        tttt = ""
        zzz = 0
        for x, y, w, h in result:    
            if x==0 and y==0 and w==0 and h==0:
                tttt += "."
                continue
            digit = cv2.resize(imgU.getNpImg()[y:y+h, x:x+w], (charW, charH))
            
            zzz+=1
            res = []
            for key in temps:
                # TODO 改为计算相同的数量比
                res.append((key, self.sim(digit, temps[key])))
            res.sort(key=lambda x:x[1])
            # print(res)
            # print(str(f"{res[-1][0]}"))
            if res[-1][1] > 0.72:
                tttt+=str(f"{res[-1][0].split(':')[0]}")
        if tttt.count(".")>1:
            tttt = tttt[:-2].replace(".","") + tttt[-2:]
        if tttt.count(".")==1:
            if len(tttt)>floadLen+1 and tttt[-floadLen-1] != ".":
                tttt = tttt.replace(".","")
        # if len(tttt)>2 and tttt[0] == "0":
        #     return "8"+tttt[1:]
            # return ""
        return tttt.replace("X","")

    def sim(self, src1, src2):
        try:
            score = cv2.matchTemplate(src1, src2, cv2.TM_CCORR_NORMED)
            return score[0][0]
        except BaseException:
            return 0.0

