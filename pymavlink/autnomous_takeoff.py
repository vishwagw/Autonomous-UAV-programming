# using pymavlink to autonomous takeoff:
from pymavlink import mavutil
import time

# Connect to the flight controller
def connect_to_fc(port='/dev/ttyS0', baud=57600):
    print(f"Connecting to {port} at {baud} baud...")
    master = mavutil.mavlink_connection(port, baud=baud)
    master.wait_heartbeat()
    print("Connected to flight controller.")
    return master

# Arm the drone
def arm_vehicle(master):
    print("Arming the vehicle...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0)  # 1 = arm
    time.sleep(2)  # Wait for arming
    if master.motors_armed():
        print("Vehicle armed successfully.")
    else:
        print("Failed to arm. Check pre-arm conditions.")
        return False
    return True

# Set mode (e.g., GUIDED)
def set_mode(master, mode):
    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    print(f"Setting mode to {mode}...")
    time.sleep(1)

# Takeoff to a specified altitude
def takeoff(master, altitude):
    print(f"Taking off to {altitude} meters...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, altitude)
    time.sleep(5)  # Wait to reach altitude (adjust based on drone speed)

# Main script
def main():
    master = connect_to_fc()
    if not master:
        return

    if arm_vehicle(master):
        set_mode(master, "GUIDED")
        takeoff(master, 10)  # Takeoff to 10 meters
        print("Takeoff command sent. Check drone status.")

    master.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
