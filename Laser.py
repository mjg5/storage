#Brief Usage:
#    To enable the laser:
#        l = Laser()
#        l.enable()
#    To disable the laser:
#        l.disable()
#    To get the status of the laser:
#        status = l.status
#    To change the current of the laser:
#        l.changeCurrent(current, channel)
#        # Channel   |   Max Current
#        # 1         |   68.09
#        # 2         |   63.89
#        # 3         |   41.59
#        # 4         |   67.39
#    To calibrate the laser using automatic windows:
#        center, secondary = l.calibrateLaser(image, mode, resolution)
#    To calibrate the laser using manual windows:
#        center, secondary = l.calibrateLaser(image, mode, resolution, cPoint,
#                                             sPoint, cSize, sSize)
#        # see the function itself for more specific information about calibration    

import serial as s
import time
from ImageProcessing import fit_gauss_2D
import numpy as np
from matplotlib import pyplot as plt

class Laser:
    
    def __init__(self, port, BaudRate, DataBits, StopBits):
        """
        Creats an instance of the Laser class. Creates a port attribute to
        hold the connection to the laser.
        """
        self.port = s.Serial('port' = port, 'baudrate' = BaudRate, 
                             'bytesize' = DataBits, 'stopbits' = StopBits)
        self.current = None
        self.channel = None
        self.status = None
    
    def enable(self, enableStatus):
        """
        Enables the laser.
        """
        self.port.open()
######################
        ###### fprintf(F, '%s\r','system = 1')
        self.port.write('system=1'.encode('utf-8'))
        self.status = 'enabled'
        print('Laser is now enabled')
        self.port.close()
        time.sleep(3)
        
    def disbale(self):
        """
        Disables the laser.
        """
        self.port.open()
###############
        #### similar questions as above
        self.port.write('enable=0'.encode('utf-8'))
        self.port.write('system=0'.encode('utf-8'))
        self.status = 'disabled'
        print('Laser is now disabled')
        self.port.close()
        time.sleep(3)
        
    def status(self):
        """
        Gets the status of the laser and returns it.
        """
        self.port.open()
        self.port.write('statword?'.encode('utf-8'))
        time.sleep(2)
        while self.port.in_waiting > 0:
            statword += self.port.read(1)
        time.sleep(1)
        self.status = statword
        self.port.close()
        return statword
    
    def changeCurrent(self, current, channel):
        """
        Chagces the current (in mA) of a specific channel of the laser
        """
        self.port.open()
        
        if channel == 1:
            max_current = 68.09
        elif channel == 2:
            max_current = 63.89
        elif channel == 3:
            max_current = 41.59
        elif channel == 4:
            max_current = 67.39
        else:
            print('No Way! channel shall be 1, 2, 3, or 4 only!')
            max_current = 0
            
        if power > max_current:
            print('No Way! power must be less than ' + max_current + ' mA only.')
        elif power == 0:
            self.port.write(('channel=' + channel).encode('utf-8'))
            time.sleep(2)
            self.port.write('enable=0'.encode('utf-8'))
            time.sleep(1)
        else:
            self.port.write(('channel=' + channel).encode('utf-8'))
            self.channel = channel
            time.sleep(2)
            self.port.write(('enable=' + channel).encode('utf-8'))
            self.status = 'enabled'
            time.sleep(2)
            self.port.write(('current=' + current).encode('utf-8'))
            self.current = current
            time.sleep(1)
        
        self.port.close()
        
    def calibrateLaser(image, mode, resolution, os, *args):
        """
        Calibrates the laser so that the peak of the secondary pattern is
        at 90% saturation. It then returns a tuple of peak intensity, 
        x-coordinate of peak intensity, and y-coordinate of peak intensity
        for both the center and secondary pattern, even if the center is
        over saturated. If mode = 'man', the program takes four positional
        arguments: the central peak point, the secondary peak point, the 
        side length of the central peak square, and the side length of the 
        secondary peak sqaure. Resoultion should be 11 or 12, with 12 being
        better resolution. 
        """
        # the following code is used for loading the simulation image
        # Note: should be removed in the final code, along with the os
        # parameter
        if image == 0:
            if os == 'windows':
               image = np.loadtxt(
                       '//mac/Home/Desktop/ripple3_256x256_ideal_undersized.txt')
            elif os == 'mac':
                image = np.loadtxt(
                        '/Users/matthewgrossman/Desktop/ripple3_256x256_...ideal_undersized.txt')
        # transposes the image so it is oriented correctly
        image = np.transpose(image)
        # places the original image at the center of a solid black image 
        # with dimensions N x N to increase the resolution of the transform.
        N = 2**resolution
        largeImage = np.zeros((N, N))
        x = np.ma.size(image, 0)
        y = np.ma.size(image, 1)
        largeImage[int((N - x) / 2) : int((N + x) / 2),
                   int((N - y) / 2) : int((N + y) / 2)] = image
        # performs the fourier transform of the larger image.
        Fourier = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(largeImage)))
        Fourier = abs(Fourier)/np.max(np.max(abs(Fourier)))
        # determines which mode should be used to find peak intensities
        if mode == 'auto':
            center, secondary = gaussAuto(Fourier, N)
        elif mode == 'man':
            center, secondary = gaussManual(Fourier, args[0], args[1],
                                            args[2], args[3])
        else:
            print('Unknown calibration command')
        # determines the proper amount to increase the laser current from
        # the guassians and then increases the laser's current.
        scale = .9 / secondary[0]
#######
        ######## need to get current level of laser and then multiply by scale
        newCurrent = scale * self.current
        self.changeCurrent(newCurrent, self.channel)
#########
        ######### ask Christian about exact math here and what data he needs
        # returns two tuples representing the new peak intensities and
        # their locations. 
        newCenterPeak = scale * center[0]
        newSecondaryPeak = scale * secondary[0]
        reutrn (newCenterPeak, center[1], center[2]), (newSecondaryPeak, 
               secondary[1], secondary[2])
    
    def gaussManual(Fourier, cPoint, sPoint, cSize, sSize):
        """
        Locates the peak intensity and its location for both the center
        and secondary patterns given a point near each of the pattern's 
        centers and a rough area to look in. Returns this info as a three 
        value tuple for the center and for the secondary pattern.
        """
        # crops the Fourier image to get images of just the two patterns
        # Note that the y-coordinate is cropped first
        centerPat = Fourier[int(cPoint[1] - cSize/2) : int(cPoint[1] + cSize/2),
                            int(cPoint[0] - cSize/2) : int(cPoint[0] + cSize/2)]
        secondaryPat = Fourier[int(sPoint[1] - sSize/2) : int(sPoint[1] + sSize/2),
                               int(sPoint[0] - sSize/2) : int(sPoint[0] + sSize/2)]
        # The following code simply finds the maximum intensity and its
        # location in each image without finding the gaussian.
#            icenterheight = np.amax(centerPat)
#            icentercoordinates = np.where(centerPat == icenterheight)
#            isecondaryheight = np.amax(secondaryPat)
#            isecondarycoordinates = np.where(secondaryPat == isecondaryheight)
#            ix1 = int(icentercoordinates[1] + cPoint[0] - cSize/2)
#            iy1 = int(icentercoordinates[0] + cPoint[1] - cSize/2)
#            ix2 = int(isecondarycoordinates[1] + sPoint[0] - sSize/2)
#            iy2 = int(isecondarycoordinates[0] + sPoint[1] - sSize/2)
        # Gets the paramenters of the gaussian for both patterns
        centerParams = fit_gauss_2D(centerPat)
        secondaryParams = fit_gauss_2D(secondaryPat)
        centerheight = centerParams[0]
        centerX = centerParams[1]
        centerY = centerParams[2]
        secondaryHeight = secondaryParams[0]
        secondaryX = secondaryParams[1]
        secondaryY = secondaryParams[2]
        # converts the coordinates in the cropped image into those of the 
        # original one. 
        x1 = int(centerX + cPoint[0] - cSize/2)
        y1 = int(centerY + cPoint[1] - cSize/2)
        x2 = int(secondaryX + sPoint[0] - sSize/2)
        y2 = int(secondaryY + sPoint[1] - sSize/2)
        print ((centerheight, x1, y1), (secondaryHeight, x2,
               y2))
#            print(icenterheight, (ix1, iy1), isecondaryheight,
#                  (ix2, iy2))
        return (centerheight, x1, y1), (secondaryHeight, x2,
               y2)
        
    def gaussAuto(Fourier, n):
        """
        Calls GaussManual using arguments that usually closely identify 
        the peak intensities. The choice in arguments is based on the
        resolution of the image. Returns the same values as GaussManual
        """
        # Note: this function could potentially be expanded to other 
        # resolutions by multiplying the parameters by a power of 2
        if n == 11:
            center, secondary = GaussManual(Fourier, (1025, 1025), 
                                            (950, 1025), 85, 34)
        elif n == 12:
            center, secondary = GaussManual(Fourier, (2050, 2050),
                                            (1900, 2050), 170, 68)
        return center, secondary