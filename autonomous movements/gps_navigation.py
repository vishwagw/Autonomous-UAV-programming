# gps based navigation for autonomous movements:
# code structure is only for movements, excluding obstacle avoidance
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

# takeoff:
def arm_and_takeoff(target_altitude):
    """
    Arms the drone and takes off to the target altitude.
    """
    print("Arming motors...")
    autumn1.mode = VehicleMode("GUIDED")
    autumn1.armed = True

    while not autumn1.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off...")
    autumn1.simple_takeoff(target_altitude)

    while True:
        print(f"Altitude: {autumn1.location.global_relative_frame.alt:.2f}m")
        if autumn1.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Target altitude reached!")
            break
        time.sleep(1)
# navigate to a specific loaction:
def goto_loc(lat, lon, alt):
    print(f"Navigating to: Lat={lat}, Lon={lon}, Alt={alt}m")
    point = LocationGlobalRelative(lat, lon, alt)
    autumn1.simple_goto(point)

# landing:
def land():
    print("vehicle is landing..")
    autumn1.mode = VehicleMode("LAND")

# initialize the program:
if __name__ == "__main__":
    arm_and_takeoff(4) # meter high
    goto_loc() # include coordinates for lat, lon, alt
    time.sleep(5) # hoover on waypoint
    land() 

    # terminate the function:
    autumn1.close()

# multiple waypoints:
#waypoints = [(), (), ()] # include coordinates here
#for lat, lon, alt in waypoints:
#    goto_loc(lat, lon, alt)
