from time import sleep
from pyairdrone.aiDrone import *

if __name__ == '__main__' :
    aidrone = AIDrone()
    aidrone.Open("COM3")
    aidrone.setOption(0)
    sleep(0.5)
            
    aidrone.motor(0, 10)
    sleep(2)
    aidrone.motor(1, 20)
    sleep(2)
    aidrone.motor(2, 20)
    sleep(2)
    aidrone.motor(3, 20)
    sleep(2)
    aidrone.Close()


