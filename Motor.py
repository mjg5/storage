class Motor:
    
    def __init__(self):
        self.figure = plt.figure(1)
        plt.title('Camera Stage APT GUI')
        self.stage
        self.ctrl
        
    def initialize(self):
        pass
    def pos(self):
        pass
    def goto_wait(self, position):
        pass
    def goto(self, position):
        pass
    def goto_home(self):
        pass
    def stop(self):
        pass
    def get_vel(self):
        pass
    def set_vel(self, vel, *args):
        pass
    def get_accel(self):
        pass
    def set_accel(self, accel):
        pass
    def wait_free(self, one, two):
        pass
    def cleanup(self):
        pass
