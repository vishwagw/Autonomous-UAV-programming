from time import sleep
from pyaidrone.aiDrone import *
from pyaidrone.deflib import *
from pyaidrone.ikeyevent import *

Height = 70
Degree = 0

if __name__ == '__main__':
    aidrone = AIDrone()
    ikey = IKeyEvent()
    aidrone.Open("COM3")
    aidrone.setOption(0)
    sleep(0.5)

    while not ikey.isKeyEscPressed():
        
        if ikey.isKeyEnterPressed():             
            aidrone.takeoff()

        if ikey.isKeySpacePressed():
            aidrone.landing()
      
        if ikey.isKeyUpPressed():
            aidrone.velocity(FRONT, 100)
        elif ikey.isKeyDownPressed():
            aidrone.velocity(BACK, 100)
        else:
            aidrone.velocity(FRONT, 0)

        if ikey.isKeyRightPressed():
            aidrone.velocity(RIGHT, 100)
        elif ikey.isKeyLeftPressed():
            aidrone.velocity(LEFT, 100)
        else:
            aidrone.velocity(RIGHT, 0) 
        
        if ikey.isKeyWPressed():
            Height = Height + 10
            aidrone.altitude(Height)
        elif ikey.isKeyXPressed():
            Height = Height - 10
            aidrone.altitude(Height)

        if ikey.isKeyDPressed():
            Degree = Degree + 10
            aidrone.rotation(Degree)            
        elif ikey.isKeyAPressed():
            Degree = Degree +10
            aidrone.rotation(-Degree)            

        sleep(0.1)
        
aidrone.Close()
