import matplotlib as mpl
from matplotlib import pyplot as plt
import win32com.client

class Motor:
    
    def __init__(self):
        self.figure = None
        self.stage = None
        self.ctrl = None
        self.motor_id = 0
        
    def connect(self):
        # create controls
        plt.close('all')
        self.figure = plt.figure(figsize = (650, 450))
        plt.title('Camera Stage APT GUI')
        # start system
        self.ctrl = win32com.client.Dispatch('MG17SYSTEM.MG17SystemCtrl.1')
        self.ctrl.StartCtrl()
        a, n_motor = self.ctrl.GetNumHWUnits(6,0)
        if n_motor == 0:
            print('No motors found!')
#        if n_motor != 1:
#            print('Wrong number of motors found...')
        serial_number = '45862339'
        self.stage = win32com.client.Dispatch('MGMOTOR.MGMotorCtrl.1')
        self.stage.HWSerialNum = serial_number
        self.stage.StartCtrl()
        self.stage.Identify()
        
    def pos(self):
        return self.stage.GetPosition_Position(self.motor_id)
    
    def goto_wait(self, position):
        self.stage.SetAbsMovePos(self.motor_id, position)
        self.stage.MoveAbsolute(self.motor_id, True)
    
    def goto(self, position):
        self.stage.SetAbsMovePos(self.motor_id, position)
        self.stage.MoveAbsolute(self.motor_id, False) 
        
    def goto_home(self):
        self.stage.MoveHome(self.motor_id, True)
        
    def stop(self):
########### not working in original code
        pass
    
    def get_vel(self):
        status, min_v, accel, max_v = self.stage.GetVelParams(self.motor_id,
                                                              0,0,0)
        return max_v
    
    def set_vel(self, vel, *args):
        pass
    def get_accel(self):
        pass
    def set_accel(self, accel):
        pass
    def wait_free(self, one, two):
        pass
    def cleanup(self):
        self.ctrl.StopCtrl()
        self.stage.StopCtrl()
