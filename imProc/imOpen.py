#modeule for getting the file type and opening the image 
#and reading from the header file info to get useful data
#aboput the image for use by other functions

from osgeo import gdal
import cv2
import re
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#function for getting the type of image
def imType(path):
    ImageExtnInfo=None
    isSat=0
    if path!=None and path!="":
        satEtx=['.tiff','.img','.lan']
        ordEtx=['jpg','jpeg','bmp','gif',]
        
        ext=re.findall('[.]\S+', path)
        
        ImageExtnInfo=None
        isSat=0
        
        for e in satEtx:
            if e==ext[0]:
                ImageExtnInfo=ext[0]
                isSat=1
            
        for e in ordEtx:
            if e==ext[0]:
                ImageExtnInfo=ext[0]
                isSat=0
    else:
        print("Invalid file format")
    
    return ImageExtnInfo,isSat

#Function to calculate number of bands
def numBands(path,isSat):
    bands=0
    if ~isSat:
        bands=1
    else:
        try:
            image=gdal.Open()
        except IOError:
            print "Could not open file"
            bands=0
        else:
            bands=image.RasterCount
    
    return bands

#function to convert file format
#def imConvert(path,newExt):
    #imExtInfo=imType(path)
    
    #satEtx=['.tiff','.img','.lan']
    
   # if newExt in satEtx:
        
