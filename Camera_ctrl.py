# camera_ctrl - provides basic control of QSI RS 6.1s CCD camera
#
# Matthew Grossman from Princeton HCIL - Jun. 5, 2018
# Based on a Matlab version developed by He Sun
#
#Brief Usage:
#    Turn on the camera and enable the handle:
#        h = Camera_ctrl(0, 'enable')
#    Initilialization:
#        Camera_ctrl(h, 'init', temperature) # temperature range: (-50, 50)
#    Stop fan and cooler:
#        Camera_ctrl(h, 'finalize')
#    Disable the handle:
#        Camera_ctrl(h, 'finalize')
#    Open or close shutter:
#        h = Camera_ctrl(h, 'shutter', openflag) 
#        # openflag: True for open, False for close
#    Set readout speed: Camera_ctrl(h, 'readoutspeed', readoutflag)
#        # readout flag: 1 for fast readout, 0 for high image quality
#    Exposure properties:
#        Camera_ctrl(h, 'exposureproperties', start_pos, size_pixels,
#                    bin_pixels)
#            # the last three inputs are all 2 tuples with default values of 
#            # (0,0), (2758, 2208), and (1,1)
#    Set shutter priority: Camera_ctrl(h, 'shutterpriority', shutterflag)
#        # shutterflag: 0 for mechanical, 1 for electrical
#    Take pictures: img = Camera_ctrl(h, 'exposure', exptime)
#        # exptime is the exposure time you can change
#    Show camera realtime picture: Camera_ctrl(h, 'realtime')
#        # can be used during calibration

from matplotlib import pyplot as plt
import numpy
import win32com.client

class Camera:
    """ A class that mimics the handle class from for cameras matlab and
    initializes to default values of serialnum: 0, shutter: open, and default
    starting position, pixel size, and bin pixels to (0,0)
       """
    def __init__(self):
        self.handle = None
        self.serialnum = '0'
        self.shutter = True
        self.startPos = (0, 0)
        self.imgSize = (0, 0)
        self.binPix = (0, 0)
        self.ccdtemp = None

def Camera_ctrl(camera, cmd, *args):
    
    n_argin = len(args)
    cmd = cmd.lower()
    
    if cmd == 'connect':
        try:
            # get a handle of the camera
            if camera.handle == None:
                camera.handle = win32com.client.Dispatch('QSICamera.CCDCamera')
            # connect the camera
            if camera.handle.Connected == False:
                camera.camera.Connected = True
                print('Connecting ' + camera.handle.__class__.__name__)
            else:
                print(camera.handle.__class__.__name__ + 'is already connected.')
            # get camera dfault peramters
            camera.serialnum = camera.handle.SerialNumber;
            camera.defaultsizepixels = (camera.handle.Numx, camera.handle.NumY)
            camera.defaultstartpos = (0, 0)
            camera.defaultbinpixels = (1, 1)
            camera = Camera_ctrl(camera, 'shutter', True)
        except Exception as ex:
            pass
#########
            ######## ask Christian about finding the names for these exceptions
        return camera
    
    elif cmd == 'disconnect':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        # close shutter
        camera = Camera_ctrl(camera, 'shutter', False)
        Camera_ctrl(camera, 'finalize')
        Camera_ctrl(camera, 'disable')
        print('Disconnecting ' + camera.handle.__class__.__name__)
        camera.handle = None
        return camera
    
    elif cmd == 'init':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        # sets the current camera as the main camera
        if camera.handle.IsMainCamera == False:
            camera.handle.IsMainCamera = True
        # turns on the camera fan
        if camera.handle.FanMode != 'FanFull':
            camera.handle.FanMode = 'FanFull'
        # enable the CCD cooler
        if camera.handle.CoolerOn != True:
            camera.handle.CoolerOn = True
        # set camera cooling temperature and update ccdtemp attribute
        ccdtempc = args[0]
        if camera.handle.CanSetCCDTemperature == True:
            camera.handle.SetCCDTemperature = ccdtempc
            camera.ccdtemp = camera.handle.SetCCDTemperature
        # set camera gain to low gain
        if camera.handle.CameraGain != 'CameraGainLow':
            camera.handle.CameraGain = 'CameraGainLow'
            # set camera shutter priority to electrical
            # 0 for mechanical, 1 for electical
            camera.handle.ShutterPriority = 1
            return camera
            
    elif cmd == 'shutter':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        openflag = args[0]
        if openflag == True:
            # Set the camera to manual shutter mode.
            camera.handle.ManualShutterMode = True
            # Open the shutter as specified
            camera.handle.ManualShutterOpen = True
            camera.shutter = True
        else:
            # Set the camera to manual shutter mode
            camera.handle.ManualShutterMode = True
            # Close the shutter as specified
            camera.handle.ManualShutterOpen = False
            # Set the camera to auto shutter mode
            camera.handle.ManualShutterMode = False
            camera.shutter = False;
        return camera
    
    elif cmd == 'exposureproperties':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        if n_argin != 3:
            raise ValueError('Wrong number of input arguments')
        startPos = args[0]
        imgSize = args[1]
        binPix = args[2]
        if len(startPos) != 2:
            raise ValueError('Wrong dimension of start position')
        if len(imgSize) != 2:
            raise ValueError('Wrong dimension of picture size')  
        if len(binPix) != 2:
            raise ValueError('Wrong dimension of binned pixels')
        # sends the exposure properties to the camera
        camera.handle.StartX = startPos[0]
        camera.handle.StartY = startPos[1]
        camera.handle.NumX = imgSize[0]
        camera.handle.NumY = imgSize[1]
        camera.handle.BinX = binPix[0]
        camera.handle.BinY = binPix[1]
        # update the camera attributes
        camera.startPos = (camera.handle.StartX, camera.handle.StartY)
        camera.imgSize = (camera.handle.NumX, camera.handle.Numy)
        camera.binPix = (camera.handle.BinX, camera.handle.BinY)
        return camera
    
    elif cmd == 'avgimg':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        if n_argin != 2:
            raise ValueError('Wrong number of input arguments')
        camera.handle.ReadoutSpeed = camera.fastReadout
        expTime = args[0]
        numIm = args[1]
        img = numpy.zeros((camera.imgSize[1], camera.imgSize[0]), numpy.int32)
        for i in range(numIm):
            img = img + Camera_ctrl(camera, 'exposure', expTime)
        return img / numIm
    
    elif cmd == 'exposure':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        exptime = args[0]
        # Starts an exposure on the camera
        camera.shutter.StartExposure(exptime, camera.shutter)
        # Wait for the exposure to complete
        done = camera.handle.ImageReady
        while done != True:
            done = camera.handle.ImageReady
#HOW WILL THE SAFEARRAY COME OUT?
        # gets the image from the camera as some form of array
        return camera.handle.ImageArray
    
    elif cmd == 'realtime':
        # creates the figure
        plt.figure(100)
        plt.title('Real Time Picture')
        plt.tight_layout()
        # updates the figure with the current image until the figure is closed
        while plt.fignum_exists(100):
            img = Camera_ctrl(camera, 'exposure', 0.0003)
            plt.imshow(img)
            plt.pause(.1)
        
    elif cmd == 'readoutspeed':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        readoutflag = args[0]
        # sends the readout speed to the camera
        camera.handle.ReadoutSpeed = readoutflag      
                
    elif cmd == 'shutterpriority':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        shutterflag = args[0]
        # sends the shutter pririty to the camera
        camera.handle.ShutterPriority = shutterflag

    elif cmd == 'finalize':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        # turn off the camera fan
        if camera.handle.FanMode != 'FanOff':
            camera.handle.FanMode = 'FanOff'
        # disable the CCD cooler
        if camera.handle.CoolerOn != False:
            camera.handle.CoolerOn = False
        # closes the shutter
        Camera_ctrl(camera, 'shutter', False)
        camera.shutter = False
        
    elif cmd == 'disable':
        if camera.handle == None:
            raise Exception('Camera not connected.')
        # disconnects camera
        if camera.handle.Connected == True:
            camera.handle.Connected = False
    else:
        print('unkown command: ' + cmd)