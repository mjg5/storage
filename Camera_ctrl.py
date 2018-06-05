# camera_ctrl - provides basic control of QSI RS 6.1s CCD camera
#
# Matthew Grossman from Princeton HCIL - Jun. 5, 2018
#
#Brief Usage:


import win32com.client 
import matplotlib


class Handle:
    """A class that mimics the handle class from matlab and initializes
       to the default values
       """
    def __init__(self):
        self.camera = win32com.client.Dispatch('QSICamera.CCDCamera')
        self.serialnum = '00602768'
        self.shutter = True
        self.defautstartpos = (0, 0)
        self.defaultsizepixels = (2758, 2208)
        self.defaultbinpixels = (1, 1)


def Camera_ctrl(handle, cmd, *args):
    
    n_argin = len(args)
    cmd = cmd.lower()
    
    if cmd == 'enable':
        
        handle = Handle()
        # confirms the camera is connected
        if handle.camera.Connected == False:
            handle.camera.Connected = True
        # gets the camera's serial number
        #handle.serialnum = handle.camera.SerialNumber)
        return handle
    
    elif cmd == 'init':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        # sets the current camera as the main camera
        if handle.camera.IsMainCamera == False:
            handle.camera.IsMainCamera = True
        # turn on the camera fan
        if handle.camera.FanMode != 'FanFull':
            handle.camera.FanMode = 'FanFull'
        #handle.camera.FanMode = 'FanOff'
        # enable the CCD cooler
        if handle.camera.CoolerOn != True:
            handle.camera.CoolerOn = True
        # set camera cooling temperature
#ASK ABOUT USE OF CELL2MAT HERE!!!
        ccdtempc = args[0]
        if handle.camera.CanSetCCDTemperature == True:
            handle.camera.SetCCDTemperature = ccdtempc
        # set camera gain to low gain
        if handle.camera.CameraGain != 1:
            handle.camera.CameraGain = 1
        return 1
        
    elif cmd == 'shutter':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        openflag = args[0]
        if openflag == 1:
            # Set the camera to manual shutter mode.
            handle.camera.ManualShutterMode = True
            # Open the shutter as specified
            handle.camera.ManualShutterOpen = True
            handle.shutter = 1
        else:
            # Set the camera to manual shutter mode
            handle.camera.ManualShutterMode = True
            # Close the shutter as specified
            handle.camera.ManualShutterOpen = False
            # Set the camera to auto shutter moder
            handle.camera.ManualShutterMode = False
            handle.shutter = 0;
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
#ASK WHY COMMENTED OUT
        #if ((start_pos[0] + size_pixels[0]) * (bin_pixels[0]))
          #<= defaultsizepixels[0]
            #raise ValueError('x pixels exceeds chip range!')
        #if ((start_pos[1] + size_pixels[1]) * (bin_pixels[1]))
          #<= defaultsizepixels[1]
            #raise ValueError('y pixels exceeds chip range!')
        handle.camera.StartX = start_pos[0]
        handle.camera.StartY = start_pos[1]
        handle.camera.NumX = size_pixels[0]
        handle.camera.NumY = size_pixels[1]
        handle.camera.BinX = bin_pixels[0]
        handle.camera.BinY = bin_pixels[1]
        return 1
    
    elif cmd == 'shutterpriority':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        shutterflag = args[0]
        handle.camera.ShutterPriority = shutterflag
        return 1
    
    elif cmd == 'readout speed':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        readoutflag = args[0]
        handle.camera.ReadoutSpeed =  readoutflag
        return 1
        
    elif cmd == 'exposure':
        if n_argin != 1:
            raise ValueError('Wrong number of input arguments')
        exptime = args[0]
# THIS DOESN"T SEEM RIGHT
        if handle.shutter == True or handle.shutter == False:
            raise ValueError('The shutter statue is incorrect')
        handle.camera.StartExposure(exptime, handle.shutter)
        # Wait for the exposure to complete
        status = handle.camera.ImageReady
        donestatus = True
        while status != donestatus:
            status = handle.camera.ImageReady
#HOW WILL THE SAFEARRAY COME OUT?
        return handle.camera.ImageArray
    elif cmd == 'realtime':
        pass
    elif cmd == 'finalize':
        # turn off the camera fan
        if handle.camera.FanMode != 'FanOff':
            handle.camera.FanMode = 'FanOff'
        # disable the CCD cooler
        if handle.camera.CoolerOn != False:
            handle.camera.CoolerOn = False
        Camera_ctrl(handle, 'shutter', False)
        return 1
    elif cmd == 'disable':
        # disconnect camera
        if handle.camera.Connected == True:
            handle.camera.Connected = False
        return 0
    else:
        raise ValueError('unknown command:' + cmd)
        return -1    
  