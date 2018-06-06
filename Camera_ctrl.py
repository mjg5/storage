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
from CCDCclasses import Handle

def Camera_ctrl(handle, cmd, *args):
    
    n_argin = len(args)
    cmd = cmd.lower()
    
    if cmd == 'enable':
        handle = Handle()
        # confirms the camera is connected
        if handle.camera.Connected == False:
            handle.camera.Connected = True
        # sets the default values for the camera
        handle.serialnum = '00602768'
        handle.shutter = True
        handle.defaultstartpos = (0, 0)
        handle.defaultsizepixels = (2758, 2208)
        handle.defaultbinpixels = (1, 1)
        return handle
    
    elif cmd == 'init':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        # sets the current camera as the main camera
        if handle.camera.IsMainCamera == False:
            handle.camera.IsMainCamera = True
        # turns on the camera fan
        if handle.camera.FanMode != 'FanFull':
            handle.camera.FanMode = 'FanFull'
        # enable the CCD cooler
        if handle.camera.CoolerOn != True:
            handle.camera.CoolerOn = True
        # set camera cooling temperature
        ccdtempc = args[0]
        if handle.camera.CanSetCCDTemperature == True:
            handle.camera.SetCCDTemperature = ccdtempc
        # set camera gain to low gain
        if handle.camera.CameraGain != 1:
            handle.camera.CameraGain = 1
            
    elif cmd == 'shutter':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        openflag = args[0]
        if openflag == True:
            # Set the camera to manual shutter mode.
            handle.camera.ManualShutterMode = True
            # Open the shutter as specified
            handle.camera.ManualShutterOpen = True
            handle.shutter = True
        else:
            # Set the camera to manual shutter mode
            handle.camera.ManualShutterMode = True
            # Close the shutter as specified
            handle.camera.ManualShutterOpen = False
            # Set the camera to auto shutter mode
            handle.camera.ManualShutterMode = False
            handle.shutter = False;
        return handle
    
    elif cmd == 'exposureproperties':
        if n_argin != 3:
            raise ValueError('Wrong number of input arguments')
        start_pos = args[0]
        size_pixels = args[1]
        bin_pixels = args[2]
        if len(start_pos) != 2:
            raise ValueError('Wrong dimension of start position')
        if len(size_pixels) != 2:
            raise ValueError('Wrong dimension of picture size')  
        if len(bin_pixels) != 2:
            raise ValueError('Wrong dimension of binned pixels')
        # sends the exposure properties to the camera
        handle.camera.StartX = start_pos[0]
        handle.camera.StartY = start_pos[1]
        handle.camera.NumX = size_pixels[0]
        handle.camera.NumY = size_pixels[1]
        handle.camera.BinX = bin_pixels[0]
        handle.camera.BinY = bin_pixels[1]
        
    elif cmd == 'shutterpriority':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        shutterflag = args[0]
        # sends the shutter pririty to the camera
        handle.camera.ShutterPriority = shutterflag
        
    elif cmd == 'readout speed':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        readoutflag = args[0]
        # sends the readout speed to the camera
        handle.camera.ReadoutSpeed = readoutflag      
        
    elif cmd == 'exposure':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        exptime = args[0]
        # Starts an exposure on the camera
        handle.camera.StartExposure(exptime, handle.shutter)
        # Wait for the exposure to complete
        status = handle.camera.ImageReady
        donestatus = True
        while status != donestatus:
            status = handle.camera.ImageReady
#HOW WILL THE SAFEARRAY COME OUT?
        # gets the image from the camera as some form of array
        return handle.camera.ImageArray
    
    elif cmd == 'realtime':
        # creates teh figure
        plt.figure(100)
        plt.title('Real Time Picture')
        plt.tight_layout()
        # updates the figure with the current image until the figure is closed
        while plt.fignum_exists(100):
            img = Camera_ctrl(handle, 'exposure', 0.0003)
            plt.imshow(img)
            plt.pause(.1)
            
    elif cmd == 'finalize':
        # turn off the camera fan
        if handle.camera.FanMode != 'FanOff':
            handle.camera.FanMode = 'FanOff'
        # disable the CCD cooler
        if handle.camera.CoolerOn != False:
            handle.camera.CoolerOn = False
        # closes the shutter
        Camera_ctrl(handle, 'shutter', False)
        handle.shutter = False
        
    elif cmd == 'disable':
        # disconnects camera
        if handle.camera.Connected == True:
            handle.camera.Connected = False
    else:
        raise ValueError('unknown command:' + cmd)