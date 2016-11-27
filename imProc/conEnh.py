from osgeo.gdal_array import DatasetReadAsArray
import numpy as np
import osgeo
import gdal
import cv2
import re
import math
from osgeo import osr
import os


#function for log stretch
def Imagelog(path):
    
    #accessing file
    im=gdal.Open(path)
    
    #extracting bands
    BandData=im.GetRasterBand(1)
    BandArray=BandData.ReadAsArray(0,0,None,None)
    dim=BandArray.shape
    oneMat=np.ones((dim[0],dim[1]))
    minVal=np.min(BandArray)
    BandArray=np.add(BandArray,minVal)
    maxVal=np.max(BandArray)
    BandArray=np.multiply(BandArray,255/maxVal)
    
    
    #calculating K and C
    k=255/(math.log10(1+maxVal)/(1+math.log10(1+minVal)))
    c=-1*k*math.log10(1+minVal)
    
    
    LogBandArray=k*np.log10(np.add(oneMat,BandArray))+c
    
    maxVal=np.max(LogBandArray)
    LogBandArray=np.multiply(LogBandArray,255/maxVal)
    pathSplit=path.split('\\')
    newpath=pathSplit[0]
    for x in range(1,(len(pathSplit)-1)):
        newpath=newpath+"\\"+pathSplit[x]
    
    nameSplit=pathSplit[(len(pathSplit)-1)].split('.')
    newname=nameSplit[0]+"_log"+".jpg"
    
    newpath=root+"\\user_data\\"+newname
    print newname
    print "this is the path"
    print newpath
    cv2.imwrite(newpath, LogBandArray)
    print "file written"
    return newname
