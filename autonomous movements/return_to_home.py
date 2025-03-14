# returning to home after autonomous movements
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# conencting to vehicle:
autumn1 = connect('/dev/ttyACM0', baud=115200, wait_ready=True)

# home location:
home_location = None

# takeofffunction:
def arm_takeoff(target_alt):

    global home_location

    print("Arming motors...")
    autumn1.mode = VehicleMode("GUIDED")
    autumn1.armed = True

    while not autumn1.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off...")
    autumn1.simple_takeoff(target_alt)

    while True:
        print(f"Altitude: {autumn1.location.global_relative_frame.alt:.2f}m")
        if autumn1.location.global_relative_frame.alt >= target_alt * 0.95:
            print("Target altitude reached!")
            home_location = autumn1.location.global_frame  # Save home location
            break
        time.sleep(1)

# function for go to location:
def goto_loc(lat, lon, alt):

    print(f"Navigating to: Lat={lat}, Lon={lon}, Alt={alt}m")
    point = LocationGlobalRelative(lat, lon, alt)
    autumn1.simple_goto(point)

    time.sleep(10) 

# return to home:
def return_to_home():
    global home_location
    if home_location:
        print("Returning to Home...")
        autumn1.mode = VehicleMode("RTL")  # ArduCopter has a built-in RTL mode
    else:
        print("Home location not recorded!")

#land function:
def land():

    print("Landing...")
    autumn1.mode = VehicleMode("LAND")

# initalize the program:
if __name__ == "__main__":
    arm_takeoff(4) # 4 mter alt
    goto_loc() # insert coordinates
    return_to_home()
    land()

