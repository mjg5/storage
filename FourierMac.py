# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 13:49:20 2018

@author: matthewgrossman
"""

from matplotlib import pyplot as ppl
import numpy as np
ppl.close('all')
P = np.loadtxt('/Users/matthewgrossman/Desktop/ripple3_256x256_ideal_undersized.txt')
P = np.transpose(P)
ppl.figure()
ppl.imshow(P, origin = 'lower', cmap = 'gray')

N=2**12
P1 = np.zeros((N,N))
P1[int((N-np.size(P,0))/2):int((N+np.size(P,0))/2),int((N-np.size(P,1))/2):int((N+np.size(P,1))/2)] = P

#x = np.array(P, dtype='float')
F = np.fft.fftshift(np.fft.fft2(np.fft.fftshift(P1)))

F1 = abs(F)/np.max(np.max(abs(F)))
ppl.figure()
ppl.imshow(F1, origin = 'lower', cmap = 'jet')