## get image with specific DM command
# Developed by Matthew Grossman on Jun. 6, 2018
# Based on a matlab version developed by He Sun on Feb. 23, 2017
#
# target - defines the properties of light source
# DM - defines the DM model and parameters of devices
# coronagraph - defines the coronograph type, shape and distances
# camera - defines the properties of camera, including pixel size, binning,
#    noises, and others
# darkHole - defines the dark hole region
# estimator - defines the parameters of wavefront estimator
# DM1command, DM2command - the current voltage commands of DMs
# simOrLab - 'simulation for taking simulated image, 'lab' for real ones

import numpy

def getSimImg(target, DM, coronagraph, camera, DM1command, DM2command):
    """ A function that getes a simulated image with a specific DM command"""
    # add noises to the DM volatege input
# CONFIRM THIS IS A BOOLEAN AND NOT A VALUE OF 1
    if DM.noise == True:
        voltageNoise1 = DM.DMvoltageStd * numpy.multiply(
                DM1command, numpy.random.randn(numpy.ndarray(DM1command)))
# IN ORIGINAL CODE THERE IS A DM1COMMAND HERE. SHOULD IT BE A DM2COMMAND
        voltageNoise2 = DM.DMvoltageStd * numpy.multiply(
                DM2command, numpy.random.randn(numpy.ndarray(DM1command)))
        DM1command += voltageNoise1
        DM2command += voltageNoise2
    # simulate the image
    
    
def getImg(target, DM, coronagraph, camera, DM1command, DM2command, simOrLab):
    # check the DM commands don't exceed upper limit
    if numpy.any(numpy.isnan(DM1command)):
        raise ValueError('DM COMMANDS EXCEED LIMIT!!')
    if numpy.any(numpy.isnan(DM2command)):
        raise ValueError('DM COMMANDS EXCEED LIMIT!!')
    if numpy.amax(numpy.absolute(DM1command)) > DM.voltageLimit:
        raise ValueError('DM COMMANDS EXCEED LIMIT!!')
    if numpy.amax(numpy.abs(DM2command)) > DM.voltagelimit:
       raise ValueError('DM COMMANDS EXCEED LIMIT!!')
    # take simulated or lab image
    simOrLab = simOrLab.lower()
    if simOrLab == 'simulation':
        img = getSimImg(target, DM, coronagraph, camera, DM1command,
                        DM2command)
    elif simOrLab == 'lab':
        img = getLabImg(target, DM, camera, DM1command, DM2command)
    else:
        raise ValueError('We only have two modes, simulation or lab.')
    return img