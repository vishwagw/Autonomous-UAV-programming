from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# connect vehicle:
autumn1 = connect('/dev/ttyACM0', baud=115200, wait_ready=True)

# function for take off:
def arm_takeoff(target_alt):
    print("arming the motors..")
    autumn1.mode = VehicleMode("GUIDED")
    time.sleep(1)

    while not autumn1.armed:
        print("waiting for arming..")
        time.sleep(1)

    autumn1.armed = True
    print("taking off the vehicle..")
    autumn1.simple_takeoff(target_alt)
    time.sleep(1)

    while True:
        print(f"Altitude: {autumn1.location.global_relative_frame.alt:.2f}m")
        if autumn1.location.global_relative_frame.alt >= target_alt* 0.95:
            print("Target altitude reached!")
            break
        time.sleep(1)

def landing():
    print("vehicle is landing back..")
    autumn1.mode = VehicleMode("LAND")
    
# intialize the autonomous process:
if __name__ == "__main__":
    arm_takeoff(4) # take off to 3 meter altitude from ground
    time.sleep(5) # hoover in target altitude
    landing()

    # terminating function:
    autumn1.close()

