from ImageProcessing import twoD_Gaussian
from ImageProcessing import fit_gauss_2D
import numpy as np
from matplotlib import pyplot as plt
def GaussManual(Fourier, cPoint, sPoint, cSize, sSize):
    centerPat = Fourier[int(cPoint[1] - cSize/2) : int(cPoint[1] + cSize/2),
                        int(cPoint[0] - cSize/2) : int(cPoint[0] + cSize/2)]
    secondaryPat = Fourier[int(sPoint[1] - sSize/2) : int(sPoint[1] + sSize/2),
                           int(sPoint[0] - sSize/2) : int(sPoint[0] + sSize/2)]
    icenterheight = np.amax(centerPat)
    icentercoordinates = np.where(centerPat == icenterheight)
    isecondaryheight = np.amax(secondaryPat)
    isecondarycoordinates = np.where(secondaryPat == isecondaryheight)
    ix1 = int(icentercoordinates[1] + cPoint[0] - cSize/2)
    iy1 = int(icentercoordinates[0] + cPoint[1] - cSize/2)
    ix2 = int(isecondarycoordinates[1] + sPoint[0] - sSize/2)
    iy2 = int(isecondarycoordinates[0] + sPoint[1] - sSize/2)
    centerParams = fit_gauss_2D(centerPat)
    secondaryParams = fit_gauss_2D(secondaryPat)
    centerheight = centerParams[0]
    centerX = centerParams[1]
    centerY = centerParams[2]
    secondaryHeight = secondaryParams[0]
    secondaryX = secondaryParams[1]
    secondaryY = secondaryParams[2]
    x1 = int(centerX + cPoint[0] - cSize/2)
    y1 = int(centerY + cPoint[1] - cSize/2)
    x2 = int(secondaryX + sPoint[0] - sSize/2)
    y2 = int(secondaryY + sPoint[1] - sSize/2)
    print ((centerheight, x1, y1), (secondaryHeight, x2,
           y2))
    print(icenterheight, (ix1, iy1), isecondaryheight,
          (ix2, iy2))
    return (centerheight, x1, y1), (secondaryHeight, x2,
           y2)
                   
def CalibrateLaser(image, mode, resolution, os, *args):
    if image == 0:
        if os == 'windows':
           image = np.loadtxt('//mac/Home/Desktop/ripple3_256x256_ideal_undersized.txt')
        elif os == 'mac':
            image = np.loadtxt('/Users/matthewgrossman/Desktop/ripple3_256x256_ideal_undersized.txt')
    image = np.transpose(image)
    N = 2**resolution
    largeImage = np.zeros((N, N))
    x = np.ma.size(image, 0)
    y = np.ma.size(image, 1)
    largeImage[int((N - x) / 2) : int((N + x) / 2),
               int((N - y) / 2) : int((N + y) / 2)] = image
    Fourier = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(largeImage)))
    Fourier = abs(Fourier)/np.max(np.max(abs(Fourier)))
    if mode == 'auto':
        pass
#        CalibrateLaserAuto(Fourier)
    elif mode == 'man':
        center, secondary = GaussManual(Fourier, args[0], args[1], args[2],
                                        args[3])
    else:
        print('Unknown calibration command')
    