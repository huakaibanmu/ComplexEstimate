import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from skimage.measure import compare_ssim
import xml.dom.minidom
from  xml.dom.minidom  import Document
from PIL import Image
import os
import sys

import csv



#全局复杂度量化：获得图像二维熵
def getEntropy(imp):

    matrix = np.zeros([imp.shape[0], imp.shape[1]])  # 存储某点的邻域灰度均值
    w = 3  # 相邻的范围定义
    val = 0
    sumLin = 0  # 邻域灰度求和
    count = 0  # 邻域点个数
    hist = [[0 for i in range(256)] for i in range(256)]
    map_dict = {}
    output = 0  # 信息熵
    # print(imp.shape[0])
    # print(imp.shape[1])
    for i  in range(w,imp.shape[0]-w):#逐行遍历，imp.shape[0]为矩阵行数
        for j in range(w,imp.shape[1]-w):#逐列遍历，imp.shape[1]为矩阵列数
             for p in range(i-w,i+w+1):
                  for q in range(j-w,j+w+1):
                     sumLin +=imp[p][q]#某点邻域灰度求和
                     count +=1
             matrix[i][j] = sumLin/count#邻域灰度平均值
             sumLin = 0
             count = 0
             val1 =  int(imp[i][j])
             val2 = int(matrix[i][j])
             hist[ val1][val2] += 1
    for i in range(imp.shape[0]):
        for j in range(imp.shape[1]):
            curRow = int(imp[i][j])
            curCol = int(matrix[i][j])
            N = imp.shape[0]*imp.shape[1]
            hist[curRow][curCol] =  hist[curRow][curCol]/pow(N,2)#获取概率
            if(hist[curRow][curCol]/float(N)>0):
                output -= hist[curRow][ curCol] *(math.log(hist[curRow][curCol]/float(N),10))

    return(output)
#获取峰值信噪比
def imageHandle():

    if(not os.path.exists(beforeGraphs[:-10]+'After/')):
        os.mkdir(beforeGraphs[:-10]+'After/')
    # 遍历选取文件夹内部文件

    list = os.listdir(beforeGraphs)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        Imagepath = os.path.join(beforeGraphs, list[i])
        if os.path.isfile(Imagepath):
            afterGraph = beforeGraphs[:-10]  # 'F:/SciencedataSet/3/'
            afterGraph += 'After/'  # 'F:/SciencedataSet/3/After'
            afterGraph += Imagepath[-10:]  # 'F:/SciencedataSet/3/After/******.jpg'
            parseXML = beforeGraphs[:-10]
            parseXML += 'Annotations/'
            parseXML += Imagepath[-10:-4]
            parseXML += '.xml'
            imp = cv2.imread(Imagepath, 0)
            tempImp = imp.copy()
            targetImp = np.zeros([imp.shape[0], imp.shape[1]])
            dom = xml.dom.minidom.parse(parseXML)
            # 获取目标识别框坐标
            root = dom.documentElement
            targetNum = len(root.getElementsByTagName('xmax'))
            for q in range(targetNum):
                xmax = int(root.getElementsByTagName('xmax')[q].firstChild.data)
                xmin = int(root.getElementsByTagName('xmin')[q].firstChild.data)
                ymax = int(root.getElementsByTagName('ymax')[q].firstChild.data)
                ymin = int(root.getElementsByTagName('ymin')[q].firstChild.data)
                targetImp[ymin:ymax, xmin:xmax] = 1
            for i in range(imp.shape[0]):
                for j in range(imp.shape[1]):
                    if (targetImp[i][j] == 0):
                        tempImp[i][j] = 0
            newImage = Image.fromarray(tempImp)
            newImage.save(afterGraph)
            print(str(int(20)))
def getPSNR(imp,newImp):
    MSE = 0
    psnr = 0
    #求均方误差MSE
    height = imp.shape[0]
    width = imp.shape[1]
    for i in range(height):
        for j in range(width):
            MSE += np.square(imp[i][j]-newImp[i][j])#修改局部变量，直接在函数里面声明，否则视为修改全局变量，加上global进行声明
            #图像像素值是ubyte类型，ubyte类型数据范围为0~255，若做运算9出现负值或超出255
    MSE = MSE/ (height*width)
    #求峰值信噪比PSNR
    if(MSE != 0 ):
      psnr = 10* math.log10(255*255/MSE)
      return (psnr)
#获取结构相似性
def getSSIM(beforeGraph,afterGraph):
    imageX = cv2.imread(beforeGraph, 0)
    imageY = cv2.imread(afterGraph, 0)
    (score, diff) = compare_ssim(imageX, imageY, full=True)
    return (score)
#获取噪声估计
def getNoiseEstimate(img):
    sum = 0
    fil = np.array([[1, -2, 1],  # 这个是设置的滤波，也就是卷积核
                    [-2, 5, -2],
                    [1, -2, 1]])
    res = cv2.filter2D(img, -1, fil)
    length = res.shape[1]
    height = res.shape[0]
    # width = res.shape[2]
    for i in range(height):
        for j in range(length):
            # for k in range(width):
             sum += res[i][j]
    noise = np.sqrt((math.pi / (12 * (length - 2) * (height - 2))) * sum)
    return (noise)

def getRSS(image,xmin,xmax,ymin,ymax):
    targetValue = 0
    backgroundValue = 0
    targetPixNum = 0
    backgroundPixNum = 0
    imageHeight = image.shape[0]
    imageWidth = image.shape[1]
    imp = np.array(image)
    tempImp = imp.copy()
    targetWidth = xmax - xmin
    targetHeight = ymax - ymin
    backgroundxmax = (int)(
        (xmax + targetWidth / 2) if (xmax + targetWidth / 2) < imageWidth else imageWidth)  # 如果目标临近背景超出图像范围，进行截取
    backgroundxmin = (int)((xmin - targetWidth / 2) if (xmin - targetWidth / 2) > 0 else 0)
    backgroundymax = (int)(
        (ymax + targetHeight / 2) if (ymax + targetHeight / 2) < imageHeight else imageHeight)  # 如果目标临近背景超出图像范围，进行截取
    backgroundymin = (int)((ymin - targetHeight / 2) if (ymin - targetHeight / 2) > 0 else 0)

    targetArray = np.zeros((targetHeight + 1, targetWidth + 1))  # python的二维数据表示要用二层括号来进行表示
    for i in range(backgroundymin, backgroundymax):  # shape[0]是行数
        for j in range(backgroundxmin, backgroundxmax):  # shape[1]是列数
            if (i >= ymin and i <= ymax and j >= xmin and j <= xmax):
                targetValue += imp[i][j]
                targetArray[i - ymin][j - xmin] = imp[i][j]
                targetPixNum += 1
            else:
                backgroundValue += imp[i][j]
                backgroundPixNum += 1
    stanDeviation = np.std(targetArray)  # 计算目标内部标准差
    if (targetPixNum != 0 and backgroundPixNum != 0):
        targetValue /= targetPixNum
        backgroundValue /= backgroundPixNum
    RSS = (np.square(targetValue - backgroundValue) + np.square(stanDeviation)) ** 0.5
    return (RSS)
#获取熵差

def getEntropyDiff(image,xmin,xmax,ymin,ymax):
    targetWidth = xmax - xmin
    targetHeight = ymax - ymin
    imageHeight = image.shape[0]
    imageWidth = image.shape[1]
    backgroundxmax = (int)(
        (xmax + targetWidth / 2) if (xmax + targetWidth / 2) < imageWidth else imageWidth)  # 如果目标临近背景超出图像范围，进行截取
    backgroundxmin = (int)((xmin - targetWidth / 2) if (xmin - targetWidth / 2) > 0 else 0)
    backgroundymax = (int)(
        (ymax + targetHeight / 2) if (ymax + targetHeight / 2) < imageHeight else imageHeight)  # 如果目标临近背景超出图像范围，进行截取
    backgroundymin = (int)((ymin - targetHeight / 2) if (ymin - targetHeight / 2) > 0 else 0)
    targetImp = image[ymin:(ymax + 1), xmin:(xmax + 1)]
    targetEntropy = getEntropy(targetImp)
    targetBgImp = image[backgroundymin:(backgroundymax + 1), backgroundxmin:(backgroundxmax + 1)]
    targetBgEntropy = getEntropy(targetBgImp)
    EntropyDiff = np.fabs(targetBgEntropy - targetEntropy)
    return (EntropyDiff)

def getEdgeRatio(img,xmin,xmax,ymin,ymax):

    img = cv2.GaussianBlur(img, (3, 3), 0)
    rawImg = cv2.Canny(img, 150, 170)
    edgeValue = 0
    for i in range(ymin, ymax):
        for j in range(xmin, xmax):
            edgeValue += rawImg[i][j]
    area = (xmax - xmin + 1) * (ymax - ymin + 1) * 4  # 邻近区域面积
    edgeRatio = edgeValue / area
    return (edgeRatio)

def transNormal(array):
    min = 0
    max = 0
    num = len(array)
    min = np.min(array)
    max = np.max(array)
    for i in range(num):
        array[i] = (array[i]-min)/float(max-min)
    return (array)

def getCommplex(beforeGraph):
    # alpha1 = 0.4#全局复杂度计算-信息熵H权重
    # alpha2 = 0.3#全局复杂度计算-峰值信噪比PSNR权重
    # alpha3 = 0.2#全局复杂度计算-结构相似性SSIM权重
    # alpha4 = 0.1#全局复杂度计算-噪声估计权重
    # belta1 = 0.3#局部复杂度计算-对比度差异权重
    # belta2 = 0.3#局部复杂度计算-信息熵差权重
    # belta3 = 0.3#局部复杂度计算-边缘比率权重
    # alpha = 0.3#全局复杂度权重
    # belta = 0.3#局部复杂度权重
    # garma = 0.3#目标数权值
    RSSMean = 0
    entropyDiffMean = 0
    edgeRatioMean = 0
#遍历选取文件夹内部文件
    afterGraph = beforeGraph[:-21]  # 'F:/SciencedataSet/3/'
    afterGraph += 'After/'  # 'F:/SciencedataSet/3/After'
    afterGraph += beforeGraph[-10:]  # 'F:/SciencedataSet/3/After/******.jpg'
    image = cv2.imread( beforeGraph, 0)
    parseXML = beforeGraph[:-21]
    parseXML += 'Annotations/'
    parseXML += Imagepath[-10:-4]
    parseXML += '.xml'
    afterImage = cv2.imread(afterGraph, 0)
    dom = xml.dom.minidom.parse(parseXML)
    # # 获取目标识别框坐标
    root = dom.documentElement
    imp = np.array(image)
    H = getEntropy(imp)  # 获取图像二维熵
    newImp = np.array(afterImage)
    PSNR = getPSNR(imp, newImp)  # 获取峰值信噪比
    SSIM = getSSIM(beforeGraph,afterGraph)  # 获取结构相似性
    noiseEstimate = getNoiseEstimate(image)
    globalNormal = transNormal([H, PSNR, SSIM, noiseEstimate])  # 全局图像复杂度特征量归一化
    globalComplex = alpha1 * globalNormal[0] + alpha2 * globalNormal[1] + alpha3 * globalNormal[2] + alpha4 * \
                    globalNormal[3]  # 图像全局复杂度
    tNum = len(root.getElementsByTagName('object'))
    for i in range(tNum):
        xmax = int(root.getElementsByTagName('xmax')[0].firstChild.data)
        xmin = int(root.getElementsByTagName('xmin')[0].firstChild.data)
        ymax = int(root.getElementsByTagName('ymax')[0].firstChild.data)
        ymin = int(root.getElementsByTagName('ymin')[0].firstChild.data)
        RSS = getRSS(image, xmin, xmax, ymin, ymax)
        entropyDiff = getEntropyDiff(image, xmin, xmax, ymin, ymax)
        edgeRatio = getEdgeRatio(afterImage, xmin, xmax, ymin, ymax)
        RSSMean += RSS
        entropyDiffMean += entropyDiff
        edgeRatioMean += edgeRatio
    if (tNum > 0):
        RSSMean /= tNum
        entropyDiffMean /= tNum
        edgeRatioMean /= tNum
    localNormal = transNormal([RSSMean, entropyDiffMean, edgeRatioMean])  # 目标局部复杂度特征量归一化
    localComplex = belta1 * localNormal[0] + belta2 * localNormal[1] + belta3 * localNormal[2]  # 目标局部复杂度
    resultComplex = alpha * globalComplex + belta * localComplex + garma * tNum
    return(resultComplex)
def getallfiles(path):
        allfile = []
        for dirpath, dirnames, filenames in os.walk(path):
            for dir in dirnames:
                allfile.append(os.path.join(dirpath, dir))
            for name in filenames:
                allfile.append(os.path.join(dirpath, name))
        return (allfile)

if __name__ =="__main__":

    # for i in range(1, len(sys.argv)):
    #     url = sys.argv[i]
    alpha1 = 0.4  # 全局复杂度计算-信息熵H权重
    alpha2 = 0.3  # 全局复杂度计算-峰值信噪比PSNR权重
    alpha3 = 0.2  # 全局复杂度计算-结构相似性SSIM权重
    alpha4 = 0.1  # 全局复杂度计算-噪声估计权重
    belta1 = 0.3  # 局部复杂度计算-对比度差异权重
    belta2 = 0.3  # 局部复杂度计算-信息熵差权重
    belta3 = 0.3  # 局部复杂度计算-边缘比率权重
    alpha = 0.3  # 全局复杂度权重
    belta = 0.3  # 局部复杂度权重
    garma = 0.3  # 目标数权值
    progress = 0
    beforeGraphs = sys.argv[1]
    imageHandle()
    pixelSum = 0#文件夹总像素值
    boxAreaSum = 0
    boxNumSum = 0
    complexSum = 0
    complexMax = 0
    complexMin = 0
# 遍历选取文件夹内部文件
    list = os.listdir(beforeGraphs)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        Imagepath = os.path.join(beforeGraphs, list[i])
        if os.path.isfile(Imagepath):
            # 编辑xml文件中的dom文档

            area = 0#框住的区域面积
            parseXML = Imagepath[:-21]
            parseXML += 'Annotations/'
            parseXML += Imagepath[-10:-4]
            parseXML += '.xml'
            dom = xml.dom.minidom.parse(parseXML)
            root = dom.documentElement
            tNum = len(root.getElementsByTagName('object'))
            boxNumSum+=tNum
            for i in range(tNum):
                xmax = int(root.getElementsByTagName('xmax')[0].firstChild.data)
                xmin = int(root.getElementsByTagName('xmin')[0].firstChild.data)
                ymax = int(root.getElementsByTagName('ymax')[0].firstChild.data)
                ymin = int(root.getElementsByTagName('ymin')[0].firstChild.data)
                area+= (xmax-xmin)*(ymax-ymin)
                boxAreaSum += area;
            doc = Document()
            ImageInfo = doc.createElement('ImageInfo')  # 创建根节点
            doc.appendChild(ImageInfo)  # 根节点插入dom树
            complexity = doc.createElement('complexity')
            ImageInfo.appendChild(complexity)
            complex = getCommplex(Imagepath)
            complexSum += complex
            if (i == 0):
                complexMin = complex
            complexMax = max(complexMax,complex)
            complexMin == min(complexMin,complex)
            complexity_value = doc.createTextNode(str(complex))
            complexity.appendChild(complexity_value)
            imp = cv2.imread(Imagepath, 0)

            resolutionRatio = doc.createElement('resolutionRatio')
            ImageInfo.appendChild(resolutionRatio)
            resolutionRatio_value = doc.createTextNode(str(imp.shape[0])+'*'+str(imp.shape[1]))
            resolutionRatio.appendChild(resolutionRatio_value)
            pixelSum += imp.shape[0]*imp.shape[1]

            height = doc.createElement('height')
            ImageInfo.appendChild(height)
            height_value = doc.createTextNode(str(imp.shape[0]) )
            height.appendChild(height_value)

            height = doc.createElement('width')
            ImageInfo.appendChild(height)
            height_value = doc.createTextNode(str(imp.shape[1]))
            height.appendChild(height_value)

            boxNum = doc.createElement('boxNum')
            ImageInfo.appendChild( boxNum)
            boxNum_value = doc.createTextNode(str(tNum))
            boxNum.appendChild( boxNum_value)

            boxArea = doc.createElement('boxArea')
            ImageInfo.appendChild(boxArea)
            boxArea_value = doc.createTextNode(str(area))
            boxArea.appendChild(boxArea_value)
            print(str(20+i/len(list)*60))
            #编辑dom文档完毕
            if (not os.path.exists(beforeGraphs[:-11]+'/ImageInfo')):
                os.mkdir(beforeGraphs[:-11]+'/ImageInfo')
            filename = beforeGraphs[:-11]+'/ImageInfo/'+ Imagepath[-10:-4]+'.xml'
            with open(filename, 'wb+') as f:
                f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
#文件夹整体信息
    pixelMean = pixelSum/len(list)#文件夹内图片的平均分辨率
    boxAreaMean = boxAreaSum/boxNumSum#文件夹内图片人物识别框平均大小
    complexMean = complexSum/len(list)
    doc2 = Document()
    ImagesFolderInfo = doc2.createElement('ImagesFolderInfo')  # 创建根节点
    doc2.appendChild(ImagesFolderInfo)  # 根节点插入dom树

    imageNum  = doc2.createElement('imageNum')
    ImagesFolderInfo.appendChild(imageNum)
    imageNum_value = doc.createTextNode(str(len(list)))
    imageNum.appendChild(imageNum_value)


    resolutionRatioMean = doc.createElement('resolutionRatioMean')
    ImagesFolderInfo.appendChild(resolutionRatioMean)
    resolutionRatioMean_value = doc.createTextNode(str(pixelMean))
    resolutionRatioMean.appendChild(resolutionRatioMean_value)

    boxMean = doc.createElement('boxAreaMean')
    ImagesFolderInfo.appendChild(boxMean)
    boxMean_value = doc.createTextNode(str(boxAreaMean))
    boxMean.appendChild(boxMean_value)

    complexityMean = doc.createElement('complexMean')
    ImagesFolderInfo.appendChild(complexityMean)
    complexityMean_value = doc.createTextNode(str(complexMean))
    complexityMean.appendChild(complexityMean_value)

    complexityMax = doc.createElement('complexMax')
    ImagesFolderInfo.appendChild(complexityMax)
    complexityMax_value = doc.createTextNode(str(complexMax))
    complexityMax.appendChild(complexityMax_value)

    complexityMin = doc.createElement('complexMin')
    ImagesFolderInfo.appendChild(complexityMin)
    complexMin_value = doc.createTextNode(str(complexMin))
    complexityMin.appendChild(complexMin_value)


    # 编辑dom文档完毕

    filename = beforeGraphs[:-11] + '/ImagesInfo.xml'
    with open(filename, 'wb+') as f:
        f.write(doc2.toprettyxml(indent='\t', encoding='utf-8'))
    print('100')

