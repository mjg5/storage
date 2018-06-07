# motor_op - provides basic control of a single Thorlabs LTS 300 motor stage.
#
# Matthew Hasselfield - Nov. 26, 2008
# Revised and tested by He Sun in Princeton HCIL - Sep. 2, 2015
# Converted from Matlab to Python by Matthew Grossman - Jun. 7, 2018
#
# Brief usage:
#   Initialization:
#       h = motor_op(0, 'init')
#   Motion:
#       # Distance ranges from 0 to 300
#       motor_op(h, 'goto', 5.4)
#       motor_op(h, 'goto_wait', 5.4) # Careful, this times out...
#       motor_op(h, 'goto_home')
#       motor_op(h, 'stop')
#       current_pos = motor_op(h, 'pos')
#
#   Velocity and acceleration control:
#       max_vel = motor_op(h, 'get_vel')
#       motor_op(h, 'set_vel', new_max_vel)
#       accel = motor_op(h, 'get_accel')
#       motor_op(h, 'set_accel', new_accel)
#
#   Clean up:
#       motor_op(h, 'cleanup')
#
# Notes:
#   You must initialize the motor before using it. The 'init' function
#   returns a 'handle' that you must pass as the first argument in all
#   subsqeuent commands. This handle is actually a structure that
#   contains a few useful fields:
#       h.stage    the activeX object for the Thorlabs control top-level.
#       h.ctrl     the activeX object for the the stage we're controlling.
#       h.figure   the handle of the hidden figure where our controls live.

from matplotlib import pyplot as plt
import numpy
import win32com.client

class MotorHandle:
    """ A class that mimics the handle class for motors from matlab and 
    initializes to default values of serialnum: 0, shutter: open, and 
    default starting position, pixel size, and bin pixels to (0,0)
    """
    def __init__(self):
        self.figure = plt.figure(1)
        plt.title('Camera Stage APT GUI')
        self.stage
        self.ctrl

def motor_op(handle, cmd, *args):
    
    n_argin = len(args)
    cmd = cmd.lower()
    
    if cmd != 'init':
        c = handle.ctrl
        h = handle.stage
        f = handle.figure
        
    motor_id = 0;
    if cmd = 'init':
        # creat controls on a hidden window
#######
        ########## update figure positions later
        ############
        handle.figure = 
        
        # Start system
        c = win32com.client.Dispatch('MG17SYSTEM.MG17SystemCtrl.1')
######### 
        ######## figure out how to incorporate the positional stuff in OG code
        handle.ctrl = c
        c.StartCtrl
        