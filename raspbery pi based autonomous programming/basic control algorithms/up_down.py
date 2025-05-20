
from time import sleep
from pyaidrone.aiDrone import *
from pyaidrone.deflib import *
       
ready = -1
       
def receiveData(packet):
    global ready
    ready = packet[7] & 0x03
            
if __name__ = '__main__':
       
    aidrone = AIDrone(recevieData)
    aidrone.Open("COM3")   # change to the your ports number
    aidrone.setOption(0)
    sleep(0.5)
            
    while ready != 0:
        sleep(0.1)
                  
        aidrone.takeoff()
        sleep(5)
        aidrone.altitude(150)    # up to the 1.5m. basic altitude is 70cm
        sleep(5)
        aidrone.altitude(50) 
        sleep(5)
        aidrone.altitude(100)
        sleep(8)
        aidrone.landing()
        sleep(3)
        aidrone.Close()
