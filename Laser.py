import serial as s
import time

class Laser:
    
    def __init__(self, port, BaudRate, DataBits, StopBits):
        self.port = s.Serial('port' = port, 'baudrate' = BaudRate, 
                             'bytesize' = DataBits, 'stopbits' = StopBits)
    
    def enable(self, enableStatus):
        self.port.open()
        if enableStatus == 'on':
######################
            ###### fprintf(F, '%s\r','system = 1')
            self.port.write('system=1'.encode('utf-8'))
            print('Laser is now enabled')
        else:
###############
            #### similar questions as above
            self.port.write('enable=0'.encode('utf-8'))
            self.port.write('system=0'.encode('utf-8'))
            print('Laser is now disabled')
        self.port.close()
        time.sleep(3)
    
    def status(self):
        self.port.open()
        self.port.write('statword?'.encode('utf-8'))
        time.sleep(2)
        