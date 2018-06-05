# camera module - provides Handle and Camera classes and some camera related
#   related functions
#
# Matthew Grossman from Princeton HCIL - Jun. 5, 2018
import win32com.client 

class Handle:
    """ A class that mimics the handle class from matlab and initializes
       to the default values
       """
    def __init__(self):
        self.camera = win32com.client.Dispatch('QSICamera.CCDCamera')
        self.serialnum = '00602768'
        self.shutter = True
        self.defautstartpos = (0, 0)
        self.defaultsizepixels = (2758, 2208)
        self.defaultbinpixels = (1, 1)
        
class Camera: 
    """ A class that represents a camera, along with its handle and actions"""
    def __init__(self):
        pass
