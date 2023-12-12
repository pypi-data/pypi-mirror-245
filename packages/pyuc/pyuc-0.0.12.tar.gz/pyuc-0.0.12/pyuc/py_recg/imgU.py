# -*- coding: UTF-8 -*-
# pip install opencv-python
import pyuc
from pyuc.py_api_b import PyApiB
if PyApiB.tryImportModule("PIL", installName="Pillow"):
    from PIL import Image,ImageFilter,ImageColor,ImageOps
# if PyApiB.tryImportModule("aircv", installName="aircv"):
#     import aircv as ac
if PyApiB.tryImportModule("cv2", installName="opencv-python"):
    import cv2
if PyApiB.tryImportModule("pytesseract", installName="pytesseract"):
    import pytesseract 
    # https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe
    # tesseract --list-langs 
import numpy as np
import random
import re
import base64
from io import BytesIO


class ImgU(PyApiB):
    """
    图片相关工具
    """
    @staticmethod
    def produce(key=None):
        return PyApiB._produce(key, __class__)
    
    def __init__(self, img=None, cachePath=None):
        self.__cachePath = None
        if cachePath == None:
            cachePath = "./imgUCache"
        self.setCachePath(cachePath)
        self.__imgPath = None
        self.__pilImg = None
        self.__npImg = []
        self.__setImg(img)

            
    def emptyCache(self):
        """ 清空缓存 """
        if self.__cachePath:
            pyuc.fileU().remove(self.__cachePath)

    def remove(self):
        self.emptyCache()
        if self.__imgPath:
            pyuc.fileU().remove(self.__imgPath)
            
    def setCachePath(self, cachePath):
        """ 设置缓存路径 """
        if self.__cachePath and self.__cachePath != cachePath:
            self.emptyCache()
        self.__cachePath = cachePath
        pyuc.fileU().mkdir(self.__cachePath)
        return self
    
    def __setImg(self, img):
        if isinstance(img,str):
            if img.startswith("data:image/"):
                # base64
                base64_data = re.sub('^data:image/.+;base64,', '', img)
                binData = base64.b64decode(base64_data)
                self.__pilImg = Image.open(BytesIO(binData))
            else:
                self.__imgPath = img
        elif isinstance(img,np.ndarray):
            self.__npImg = img
        elif img != None:
            self.__pilImg = img
        return self
    
    def initImg(self, img, cachePath=None):
        """ 构建ImgU实体 """
        if cachePath == None:
            cachePath = self.__cachePath
        else:
            self.setCachePath(cachePath)
        return ImgU(img, cachePath)
    
    def getPilImg(self):
        if self.__pilImg:
            return self.__pilImg
        elif self.__imgPath:
            self.__pilImg = Image.open(self.__imgPath)
            return self.__pilImg
        elif len(self.__npImg) > 0:
            self.__pilImg = Image.fromarray(cv2.cvtColor(self.__npImg,cv2.COLOR_BGR2RGB))
            return self.__pilImg
        else:
            return None
        
    def getNpImg(self):
        """ 获取cv2像素集 """
        if len(self.__npImg) > 0:
            return self.__npImg
        elif self.__imgPath:
            self.__npImg = cv2.imread(self.__imgPath)
            return self.__npImg
        elif self.__pilImg:
            self.__npImg = cv2.cvtColor(np.asarray(self.__pilImg.convert('RGB')),cv2.COLOR_RGB2BGR)
            return self.__npImg
        return None
    
    def getNpImgHSV(self):
        """ 获取像素集并转化为hsv """
        img_src = self.getNpImg() 
        if img_src.any():
            return cv2.cvtColor(img_src,cv2.COLOR_BGR2HSV)
        else:
            return None
        
    def getNpImgGray(self):
        """ 获取像素集并转化为gray """
        img_src = self.getNpImg() 
        if img_src.any():
            return cv2.cvtColor(img_src,cv2.COLOR_RGB2GRAY)
        else:
            return None
        
    def gray(self, splitLine=127):
        """ 黑白 """
        img_src = self.getNpImg()
        GrayImage = cv2.cvtColor(img_src,cv2.COLOR_BGR2GRAY)
        r, b = cv2.threshold(GrayImage, splitLine, 255, cv2.THRESH_BINARY)
        return self.initImg(b)
    

    def invert(self):
        """ 反色 """
        return self.initImg(ImageOps.invert(self.getPilImg()))
    

    def erode(self, splitLine=127):
        """ 腐蚀（会先转化为黑白图） """
        img_src = self.getNpImg()
        GrayImage = cv2.cvtColor(img_src,cv2.COLOR_BGR2GRAY)
        r, b = cv2.threshold(GrayImage, splitLine, 255, cv2.THRESH_BINARY)
        kk = np.ones((3,3),np.uint8)
        ero = cv2.erode(b,kk,iterations=1)
        return self.initImg(ero)

    # def getNumText(self):
    #     text = pytesseract.image_to_string(self.getPilImg(),lang="eng",config='--psm 7 -c tessedit_char_whitelist=0123456789')
    #     return text
        
    def getImgPath(self):
        """ 获取当前图片对应的路径 """
        if self.__imgPath:
            return self.__imgPath
        elif self.__pilImg:
            self.__imgPath = self.getRandomPngPath()
            self.__pilImg.save(self.__imgPath,quality=100)
            return self.__imgPath
        elif len(self.__npImg) > 0:
            self.__imgPath = self.getRandomPngPath()
            cv2.imwrite(self.__imgPath, self.__npImg)
            return self.__imgPath
        else:
            return None

    def randomPngName(self):
        return f"{''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',12))}.png"
        
    def getRandomPngPath(self):
        """ 随机获取一个图片路径 """
        return f"{self.__cachePath}/{self.randomPngName()}"
    
    def crop(self, box):
        """ 截图 box: 四元组(left, upper, right, lower) """
        w,h = self.size()
        fixBox = [*box]
        for i in range(4):
            if i%2==0:
                if fixBox[i] < 0:
                    fixBox[i] = fixBox[i] + w
                elif fixBox[i] > w:
                    fixBox[i] = w
            else:
                if fixBox[i] < 0:
                    fixBox[i] = fixBox[i] + h
                elif fixBox[i] > h:
                    fixBox[i] = h
        imgObj = self.getPilImg()
        img = imgObj.crop(fixBox)
        return self.initImg(img)
    
    def size(self):
        """ 图片宽高 """
        imgObj = self.getPilImg()
        if imgObj:
            return imgObj.size
        else:
            0,0
    
    def save(self, savePath=None, quality=100):
        """ 保存 """
        if savePath == None:
            savePath = self.getRandomPngPath()
        imgObj = self.getPilImg()
        if imgObj:
            imgObj.save(savePath,quality=quality)
     
    # def findXY(self, findImgU, similarity=0.9, inBox=None):
    #     """ 查找在图片中的坐标，findImgU """
    #     if not isinstance(findImgU, str):
    #         findImgU = self.initImg(findImgU)
    #     elif not isinstance(findImgU, ImgU):
    #         raise Exception("findImgU must instances of ImgU")
    #     if inBox:
    #         imsrc = ac.imread(self.crop(inBox).getImgPath())
    #     else:
    #         imsrc = self.getNpImg()
    #     imobj = ac.imread(findImgU.getImgPath())
    #     simi = ac.find_template(imsrc, imobj, similarity)
    #     fixP = None
    #     if simi:
    #         p = simi.get("result")
    #         if p:
    #             fixP = [*p]
    #         if fixP and inBox:
    #             fixP[0] = fixP[0]+inBox[0]
    #             fixP[1] = fixP[1]+inBox[1]
    #     return fixP
    
    def resize(self, size, filter=Image.LANCZOS):
        """ 重置宽高 """
        imgObj = self.getPilImg()
        newImg = imgObj.resize(size,filter)
        return self.initImg(newImg)
    
    def show(self):
        """ 显示图片 """
        imgObj = self.getPilImg()
        if imgObj:
            imgObj.show()
            
    def splitRGB(self):
        """ 图片按三通道分离为三张图（灰度图） """
        imgObj = self.getPilImg()
        imgRGBs = imgObj.split()
        return list(map(lambda x:self.initImg(x),imgRGBs))
    
    def filtByColor(self,minColor,maxColor):
        """ 
            过滤出在两个颜色之间的所有相素并组成一张新图 例如:
            BLUE: [110, 50, 50] ~ [130, 255, 255]
            RED: [0, 50, 50] ~ [30, 255, 255]
            GREEN: [50, 50, 50] ~ [70, 255, 255]
        """
        img_src = self.getNpImg() 
        img_hsv = self.getNpImgHSV()
        _mask = cv2.inRange(img_hsv, np.array(minColor), np.array(maxColor))
        img_filt = cv2.bitwise_and(img_src, img_src, mask=_mask)
        # _savePath = self.getRandomPngPath()
        # cv2.imwrite(_savePath, img_filt)
        return self.initImg(img_filt)
        
    
    def blur(self,times=1):
        """ 对图片进行模糊效果 """
        if times < 1:
            return self
        imgObj = self.getPilImg()
        imgBLUR = imgObj
        for i in range(times):
            imgBLUR = imgBLUR.filter(ImageFilter.BLUR)
        return self.initImg(imgBLUR)
    
    def binary(self, threshold=128):
        """ 二值化图片 """
        imgObj = self.getPilImg()
        bImg = imgObj.convert("L")
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        bImg = bImg.point(table, '1')
        return self.initImg(bImg)
    
    def findCircle(self,dp=1,minDist=50,param1=10,param2=10,minRadius=50,maxRadius=100):
        """ 查找图片中的圆 """
        # [(x,y,r)]
        gray = self.getNpImgGray()
        circles1 = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,dp, 
                minDist,param1=param1,param2=param2,minRadius=minRadius,maxRadius=maxRadius) 
        try:
            if circles1.any():
                circles = circles1[0,:,:] 
                cs = np.uint16(np.around(circles))
                res = []
                for c in cs:
                    res.append((c[0],c[1],c[2]))
                return res
        except Exception as e:
            pass
        return []
        
    def findContours(self):
        """ 查找图片中的物体轮廓 """
        gray = self.getNpImgGray()
        ret, binary = cv2.threshold(gray,127,255,cv2.THRESH_BINARY) 
        contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 
        return contours
        
    def drawContours(self, contours=None, drawColor=None, penWith=3):
        """ 画轮廓 """
        if drawColor == None:
            drawColor = (0,0,255)
        img = self.getNpImg()
        cv2.drawContours(img,contours,-1,drawColor,penWith) 
        # _savePath = self.getRandomPngPath()
        # cv2.imwrite(_savePath, img)
        return self.initImg(img)
    
    def __isSameGroup(self, gr1, gr2, minDist=100):
        """ 点集是否相隔小于等于minDist """
        absMinDist = abs(minDist)
        for g1 in gr1:
            if len(g1) == 1:
                g1 = g1[0]
            if len(g1) == 1:
                g1 = g1[0]
            for g2 in gr2:
                if len(g2) == 1:
                    g2 = g2[0]
                if len(g2) == 1:
                    g2 = g2[0]
                if abs(g1[0]-g2[0]) <= absMinDist and abs(g1[1]-g2[1]) <= absMinDist:
                    return True
        return False
    
    def __getPointsCenter(self, gr, minSize=50):
        """ 获取点集的中心点 """
        minX,maxX,minY,maxY = 999999,-1,999999,-1
        for g1 in gr:
            if len(g1) == 1:
                g1 = g1[0]
            minX = min(g1[0],minX)
            maxX = max(g1[0],maxX)
            minY = min(g1[1],minY)
            maxY = max(g1[1],maxY)
        if abs(maxX-minX) < minSize and abs(maxY-minY) < minSize:
            return None
        return int(minX+maxX)>>1, int(minY+maxY)>>1
    
    def findObjPosition(self,minDist=200,minSize=10):
        """ 查找物体的中心坐标[(x,y)] minDist:物体间最小距离 """
        contours = self.findContours()
        if len(contours) < 1:
            return []
        res = []
        groupTypes = {}
        groupRes = {}
        if len(contours) > 1:
            newContours = {}
            for i in range(len(contours)-1):
                iG = groupTypes.get(str(i))
                if iG == None:
                    iG = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',12))
                    groupTypes[str(i)] = iG
                if iG not in newContours:
                    newContours[iG] = list(contours[i])
                for j in range(i+1,len(contours)):
                    if self.__isSameGroup(contours[i],contours[j],minDist=minDist):
                        newContours[iG] += list(contours[j])
                        groupTypes[str(j)] = iG
                    elif j == len(contours)-1 and i == len(contours)-2:
                        newContours[''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',12))] = list(contours[j])
            contours = list(newContours.values())
        for contour in contours:
            center = self.__getPointsCenter(contour,minSize=minSize)
            if center:
                res.append(center)
        return res
    
    def drawCircle(self, circles, drawColor=None, penWith=3):
        """ 画圆形 """
        if drawColor == None:
            drawColor = (0,0,255)
        img = self.getNpImg()
        for circle in circles:
            cv2.circle(img,(circle[0],circle[1]),circle[2],drawColor,penWith) 
        return self
         
    def drawPoints(self, points, drawColor=None, pointSize=3):
        """ 画一些点 """
        if drawColor == None:
            drawColor = (0,0,255)
        img = self.getNpImg()
        for point in points:
            cv2.circle(img,point,pointSize,drawColor,4) 
        return self
    
    def drawRectangle(self, ltPoint, rbPoint, drawColor=None, penWith=3):
        """ 画一个矩阵 """
        if drawColor == None:
            drawColor = (0,0,255)
        img = self.getNpImg()
        cv2.rectangle(img, ltPoint, rbPoint, drawColor, penWith)
        return self
    
    def drawText(self, text, ltPoint, font=cv2.FONT_HERSHEY_SIMPLEX, fontSize=2, drawColor=None, penWith=3):
        """ 画文本 """
        if drawColor == None:
            drawColor = (0,0,255)
        img = self.getNpImg()
        cv2.putText(img, text=text, org=ltPoint,fontFace=font,fontScale=fontSize,color=drawColor,thickness=penWith)
        return self
    
    def color(self, points):
        """ 获取颜色值：BGR """
        img = self.getNpImg()
        return tuple(img[points[1],points[0]])

    # def rgb2hsv(self, rgb):
    #     # 将RGB值的范围从0-255映射到0-1
    #     r, g, b = rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0
    #     cmax = max(r, g, b)
    #     cmin = min(r, g, b)
    #     delta = cmax - cmin
    #     # 计算色调（H）
    #     if delta == 0:
    #         h = 0
    #     elif cmax == r:
    #         h = ((g - b) / delta) % 6
    #     elif cmax == g:
    #         h = (b - r) / delta + 2
    #     elif cmax == b:
    #         h = (r - g) / delta + 4
    #     h = h * 60
    #     # 计算饱和度（S）
    #     if cmax == 0:
    #         s = 0
    #     else:
    #         s = delta / cmax
    #     # 计算亮度（V）
    #     v = cmax
    #     return (h, s, v)


    # def hsv2rgb(self, color):
    #     return ImageColor.getcolor("rgb", color)
    
    def hsvDist(self, hsv0, hsv1):
        """ 两个hsv的距离 """
        dh = min(abs(hsv1[0]-hsv0[0]), 360-abs(hsv1[0]-hsv0[0])) / 180.0
        ds = abs(hsv1[1]-hsv0[1])
        dv = abs(hsv1[2]-hsv0[2]) / 255.0
        return (dh**2+ds**2+dv**2)**0.5
        
    def rgbDist(self, rgb0, rgb1):
        """ 两个rgb的距离 """
        R_1,G_1,B_1 = rgb0
        R_2,G_2,B_2 = rgb1
        rmean = (R_1 + R_2 ) / 2
        R = R_1 - R_2
        G = G_1 - G_2
        B = B_1 - B_2
        return ((2+rmean/256)*(R**2)+4*(G**2)+(2+(255-rmean)/256)*(B**2))**0.5

    def fixShuffle(self, x:int, y:int, pos:list):
        """ 处理断图
            x: x轴等分数， y: y轴等分数， pos：等分后各个子图对应的序号
            例如：
            x=5, y=2, "pos"=[7, 0, 3, 1, 5, 6, 8, 4, 9, 2]
        """
        w, h = self.size()
        wC, hC = w/x, h/y
        cutImgs = [None]*len(pos)
        ii = -1
        for hi in range(y):
            sh = int(round(hi*hC,0))
            eh = int(round((hi+1)*hC,0))
            for wi in range(x):
                ii += 1
                sw = int(round(wi*wC,0))
                ew = int(round((wi+1)*wC,0))
                cutImgs[pos.index(ii)] = self.getPilImg().crop((sw, sh, ew, eh))
        newImg = Image.new(self.getPilImg().mode, (w, h))
        ii = -1
        for hi in range(y):
            sh = int(round(hi*hC,0))
            eh = int(round((hi+1)*hC,0))
            for wi in range(x):
                ii += 1
                sw = int(round(wi*wC,0))
                ew = int(round((wi+1)*wC,0))
                newImg.paste(cutImgs[ii], (sw, sh))
        return ImgU(newImg)

    