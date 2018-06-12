## initialize the camera drivers
# Developed by Matthew Grossman on Jun. 6, 2018
# Based on a Matlab version developed by He Sun

from CCDCclasses import Camera
import Camera_ctrl


# creates a new camera object
camera = Camera()

# connects the computer to camera and saves the handle
camera.handle = Camera_ctrl(0, 'enable')
# enables the camera and sets up its temperature
Camera_ctrl(camera.handle, 'init', -15)
# sets shutter priority to electrical and opens the shutter
Camera_ctrl(camera.handle, 'shutterpriority', 1)
camera.handle = Camera_ctrl(camera.handle, 'shutter', 1)
# sets up the camera properties
Camera_ctrl(camera.handle, 'exposureproperties', camera.startPosition,
            camera.imageSize, [camera.binXi, camera.binEta])
# take new dark frame if needed
if camera.newDarkFrame() == True:
    numIm = 30
    camera.darkFrame = takeDarkCam(camera.handle, camera.exposrure, numIm,
                                   camera.binXi, camera.binEta)
else:
    camera.darkFrame = darkCam