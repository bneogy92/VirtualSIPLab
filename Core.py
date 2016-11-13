
from osgeo.gdal_array import DatasetReadAsArray
import numpy as np
import osgeo
import gdal
import cv2
import re
from osgeo import osr


#Global variables for cropping function
refPt = []
cropping = False

#Function for identifying image extension
def ImageExt(path):
    if path!=None and path!="":
        satEtx=['.tiff','.img','.lan']
        ext=re.findall('[.]\S+', path)
        ImageExtnInfo=None
        for e in satEtx:
            if e==ext[0]:
                ImageExtnInfo=ext[0]
    else:
        print("Invalid file format")
    
    return ImageExtnInfo            


#Function for reading the image from the input file path if it is a valid satellite image
def ReadImage(path,ImageExtnInfo):
    print "i am in readImge"
    print path
    print ImageExtnInfo    
    if path!=None and ImageExtnInfo!=None:
        print "i am trying"
        try:
            print "i am opening file"
            image=gdal.Open(path)
            print(type(image))
            if isinstance(image, (gdal.Dataset)):
                print "file opened"
        except RuntimeError:
            print("Exception occurred while opening the file")
            image=None
        
    else:
        print "error in file"
        image=None
    
    return image


#Function to calculate number of bands
def NumBands(image):
    if isinstance(image, (gdal.Dataset)):
        bands=image.RasterCount
        print("The image has "+str(bands)+" bands")
    else:
        print("Invalid image")
        bands=None
    
    return bands

#Function to display image in conda consol
def ImageDisp(image,band):
    imageArray=DatasetReadAsArray(image)
    if isinstance(image, (gdal.Dataset)) and len(imageArray)!=0 and band!=None:
        BandData=image.GetRasterBand(band)
        BandArray=BandData.ReadAsArray(0,0,None,None)                    
        if isinstance(BandData,(osgeo.gdal.Band)) and len(BandArray)!=0:
            lowResData=BandArray[::10,::10]
            def click_and_crop(event, x, y, flags, param):
                # grab references to the global variables
                global refPt, cropping
  
                # if the left mouse button was clicked, record the starting
                # (x, y) coordinates and indicate that cropping is being
                # performed
                if event == cv2.EVENT_LBUTTONDOWN:
                    refPt = [(x, y)]
                    cropping = True
  
                # check to see if the left mouse button was released
                elif event == cv2.EVENT_LBUTTONUP:
                    # record the ending (x, y) coordinates and indicate that
                    # the cropping operation is finished
                    refPt.append((x, y))
                    cropping = False
  
                    # draw a rectangle around the region of interest
                    cv2.rectangle(lowResData.astype(np.uint8), refPt[0], refPt[1], (255, 255, 255), 10)
                    cv2.imshow(str("Low Resolution Image of Band"+str(1)), lowResData)

            clone=lowResData.copy()
            cv2.namedWindow(str("Low Resolution Image of Band"+str(1)), cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(str("Low Resolution Image of Band"+str(1)), click_and_crop)
 
            #keep looping until the 'q' key is pressed
            while True:
                # display the image and wait for a keypress
                cv2.imshow(str("Low Resolution Image of Band"+str(1)),lowResData)
                key = cv2.waitKey(1) & 0xFF
 
                # if the 'r' key is pressed, reset the cropping region
                if key == ord("r"):
                    image = clone.copy()
 
                # if the 'c' key is pressed, break from the loop
                elif key == ord("c"):
                    break 
                # if there are two reference points, then crop the region of interest
                # from the image and display it
            if len(refPt) == 2:
                roi = clone[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                cv2.imshow("ROI", roi)
                cv2.waitKey(0)

            cv2.destroyAllWindows()            
        else:
            print("No data found")
    else:
        print("Not a valid image file")
        
#function to convert file format
def convert(path,name,new,ext):
    fullpath=path+"\\"+name
    print fullpath
    im=gdal.Open(fullpath)
    BandData=im.GetRasterBand(1)
    BandArray=BandData.ReadAsArray(0,0,None,None)
    #fname=name.split('.')[0]+"."+ext
    nName=new+"."+ext
    fpath=path+"\\"+nName
    print fpath
    cv2.imwrite(fpath, BandArray)
    print fpath
    return nName


def GetGeoInfo(FileName):
    SourceDS = gdal.Open(FileName)
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())    
    return GeoT, Projection

#log stretch
def Imagelog(path):
    im=gdal.Open(path)
    
    BandData=im.GetRasterBand(1)
    BandArray=BandData.ReadAsArray(0,0,None,None)
    k=5
    dim=BandArray.shape
    oneMat=np.ones((dim[0],dim[1]))
    minVal=np.min(BandArray)
    BandArray=np.add(BandArray,minVal)
    maxVal=np.max(BandArray)
    BandArray=np.multiply(BandArray,255/maxVal)
    LogBandArray=k*np.log10(np.add(oneMat,BandArray))
    maxVal=np.max(LogBandArray)
    LogBandArray=np.multiply(LogBandArray,255/maxVal)
    pathSplit=path.split('\\')
    newpath=pathSplit[0]
    for x in range(1,(len(pathSplit)-1)):
        newpath=newpath+"\\"+pathSplit[x]
    
    nameSplit=pathSplit[(len(pathSplit)-1)].split('.')
    newname=nameSplit[0]+"_log"+".jpg"
    #Proj=GetGeoInfo(nameSplit)
    
    newpath=newpath+"\\"+newname
    print newname
    print newpath
    cv2.imwrite(newpath, LogBandArray)
    
    return newname
    
#code for transformation to img here


#Calling code
def main(path):
    print(path)
    #path=raw_input("Enter the file path")
    if path!=None and path!="":
        ImageExtn=re.findall('[.]\S+', path)
        ImageExtn=ImageExtn[0]
        print(ImageExtn)
        #ImageExtn=ImageExt(path)
        if ImageExtn==None:
            print("Image path provided does not hold a satellite image")
        else:
            FullImage=ReadImage(path, ImageExtn)   
            BandsAvail=NumBands(FullImage)
            if BandsAvail==1:
                prompt='There is 1 band in the image. You can choose from this 1 bands to display'
            else:
                prompt="There are "+str(BandsAvail)+" bands in the image. You can choose from 1-"+str(BandsAvail)+" bands to display"
                TargetBands=raw_input(prompt)
                ImageDisp(FullImage, int(TargetBands))
    else:
        print("No file path found")
    


