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
import CCDCclasses

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
###########
    ########### FINISH SIMULATING IMAGE
    ###########
    
def getLabImg(target, DM, camera, DM1command, DM2command):
    """ A function that gets a lab image with specific DM commands"""
    # Sends commands to deformable mirrors
    # flip or rotate teh DM commands
    DM1command2D = numpy.zeros((DM.Nact, DM.Nact))
    DM2command2D = numpy.zeros((DM.Nact, DM.Nact))
    DM1command2D[DM.activeActIndex] = DM1command
    DM2command2D[DM.activeActIndex] = DM2command
    DM1command2D = numpy.fliplr(DM1command2D)
    DM2command2D = numpy.rot90(DM2command2D, 2)
    DM1command = DM1command2D[DM.activeActIndex]
    DM2command = DM2command2D[DM.activeActIndex]
    # send commands to DMs
    # calculate true voltage inputs by adding command to flat voltage
    DM1VOltage = DM.DM1bias + DM1command
    DM2Voltage = DM.DM2bias + DM2command
#########
    ###########
    ########### insert code sending commands to DM driver
    ############
    # take lab image using QSI camera
    I = CCDCclasses.takeImg(camera.handle, camera.stacking, camera.exposure,
                            camera.startPosition, camera.imageSize,
                            (camera.binXi, camera.binEta))
    # check whether the camera is saturated
    if numpy.amax(I) > 3.3e5:
        raise ValueError('The camera image is saturated!! STOP!!')
    # subtract the dark frame
    I = numpy.rot90(I - camera.darkFrame, 1)
    if camera.Nxi % 2 == 0:
        xiCrop = (-camera.Nxi/2 + 1, camera.Nxi/2)
    else:
        xiCrop = (-numpy.floor(camera.Nxi/2), numpy.floor(camera.Nxi/2))
    if camera.Neta % 2 == 0:
        etaCrop = (-numpy.floor(camera.Neta/2), numpy.floor(camera.Neta/2))
    # crop the camera output to specific size
#####
    #######
    ####### need to do cropping of I still
    #########
    
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