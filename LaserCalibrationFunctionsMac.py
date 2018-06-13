from ImageProcessing import twoD_Gaussian
from ImageProcessing import fit_gauss_2D
import numpy as np
from matplotlib import pyplot as plt
def GaussManual(Fourier, cPoint, sPoint, cSize, sSize):
    centerPat = Fourier[int(cPoint[1] - cSize/2) : int(cPoint[1] + cSize/2),
                        int(cPoint[0] - cSize/2) : int(cPoint[0] + cSize/2)]
    secondaryPat = Fourier[int(sPoint[1] - sSize/2) : int(sPoint[1] + sSize/2),
                           int(sPoint[0] - sSize/2) : int(sPoint[0] + sSize/2)]
    centerParams = fit_gauss_2D(centerPat)
    secondaryParams = fit_gauss_2D(secondaryPat)
    centerheight = centerParams[0]
    centerX = centerParams[1]
    centerY = centerParams[2]
    secondaryHeight = secondaryParams[0]
    secondaryX = secondaryParams[1]
    secondaryY = secondaryParams[2]
    print((centerheight, centerX, centerY), (secondaryHeight, secondaryX,
           secondaryY))
    return (centerheight, centerX, centerY), (secondaryHeight, secondaryX,
           secondaryY)
                   
def CalibrateLaser(image, mode, resolution, *args):
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
        GuassManual(Fourier, args[0], args[1], args[2], args[3])
    else:
        print('Unknown calibration command')