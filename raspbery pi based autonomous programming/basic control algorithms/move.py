#moving the drone for a distance
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
    aidrone.move(FRONT, 200)    # 200 means 2m
    sleep(5)
    aidrone.move(BACK, 200) 
    sleep(5)
    aidrone.landing()
    sleep(3)
    aidrone.Close()

