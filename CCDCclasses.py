# camera module - provides Handle and Camera classes and some camera related
#   related functions
#
# Matthew Grossman from Princeton HCIL - Jun. 5, 2018
import win32com.client
import Camera_ctrl
import numpy
import os

class Handle:
    """ A class that mimics the handle class from matlab and initializes
       to default values of serialnum: 0, shutter: open, and default starting
       position, pixel size, and bin pixels to (0,0)
       """
    def __init__(self):
        self.camera = win32com.client.Dispatch('QSICamera.CCDCamera')
        self.serialnum = '0'
        self.shutter = True
        self.defautstartpos = (0, 0)
        self.defaultsizepixels = (0, 0)
        self.defaultbinpixels = (0, 0)
        
class Camera: 
    """ A class that represents a camera, along with its handle and actions"""
    def __init__(self):
        self.handle = Handle()
        self.startPosition
        self.imageSize
        self.binXi
        self.binEta
        self.darkFrame
        self.newDarkFrame
        self.exposure

def initializeCamera(camera):
    """ A function that initializes the camera for use"""
    # connects the computer to camera and saves the handle
    camera.handle = Camera_ctrl(0, 'enable')
    # enables the camera and sets up its temperature
    Camera_ctrl(camera.handle, 'init', -15)
    # sets shutter priority to electrical and opens the shutter
    Camera_ctrl(camera.handle, 'shutterpriority', 1)
    camera.handle = Camera_ctrl(camera.handle, 'shutter', 1)
    # sets up the camera properties
    Camera_ctrl(camera.handle, 'exposureproperties', camera.startPosition,
                camera.imageSize, (camera.binXi, camera.binEta))
    # take new dark frame if needed
    if camera.newDarkFrame() == True:
        numIm = 30
        camera.darkFrame = takeDarkCam(camera.handle, camera.exposrure, numIm,
                                   camera.binXi, camera.binEta)
    else:
# how will the darkCam file be read now? is it still a .mat file now???
        camera.darkFrame = darkCam

def finalizeCamera(camera):
    """ A function that shuts down the camera """
    camera.handle = Camera_ctrl(camera.handle, 'shutter', 0)
    Camera_ctrl(camera.handle, 'finalize')
    Camera_ctrl(camera.handle, 'disable')
    
def takeImg(h, num, exptime, start_pos, size_pixels, bin_pixels):
    """ A function that takes an image. h is a handle, num is an integer,
    start_pos, size_pixels, and bin_pixels are all tuples"""
    Camera_ctrl(h, 'exposureproperties', start_pos, size_pixels, bin_pixels)
    tempImg = numpy.zeros((size_pixels[1], size_pixels[0]), numpy.int32)
    for i in range(num):
        currentImg = Camera_ctrl(h, 'exposure', exptime)
        tempImg += currentImg
    img = (1 / num) * tempImg
    return img
    
def takeDarkCam(h_camera, exptime, numIm,  BinX, BinY):
    folder = os.getcwd()
    
    h_camera = Camera_ctrl(h_camera, 'shutter', 0)
    Camera_ctrl(h_camera, 'shuttepriority', 0)
    Camera_ctrl(h_camera, 'readoutspeed', 0)
    
    start_pos = (0, 0)
    bin_pixels = (BinX, BinY)
    size_pixels = (500, 500)
    
    darkCam = takeImg(h_camera, numIm, exptime, start_pos, size_pixels,
                      bin_pixels)
    
    os.chdir('C:\Lab\FPWC\hardware')
# ASK FORMAT FOR SAVING PICTURE. THEN SAVE HERE
    os.chdir(folder)
    return darkCam
    
