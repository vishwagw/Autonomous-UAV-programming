# this is a full test code for autunomous takeoff. hover and landing:
from pymavlink import mavutil
import time

# Connect to the flight controller
def connect_to_fc(port='/dev/ttyS0', baud=57600):
    print(f"Connecting to {port} at {baud} baud...")
    master = mavutil.mavlink_connection(port, baud=baud)
    master.wait_heartbeat()
    print("Connected to flight controller.")
    return master

# Set mode (e.g., LAND)
def set_mode(master, mode):
    mode_id = master.mode_mapping()[mode]
    master.mav.set_mode_send(
        master.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    print(f"Setting mode to {mode}...")
    time.sleep(1)

# Land the drone
def land(master):
    print("Initiating landing...")
    set_mode(master, "LAND")
    time.sleep(10)  # Wait for landing (adjust based on altitude/descent rate)
    if not master.motors_armed():
        print("Landing complete. Motors disarmed.")
    else:
        print("Landing in progress or failed. Check drone status.")

# Main script
def main():
    master = connect_to_fc()
    if not master:
        return

    land(master)

    master.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
