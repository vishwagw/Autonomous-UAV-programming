# using pymavlink for autonomous landing:
from pymavlink import mavutil
import time

# Connect to the flight controller
def connect_to_fc(port='/dev/ttyS0', baud=57600):
    print(f"Connecting to {port} at {baud} baud...")
    master = mavutil.mavlink_connection(port, baud=baud)
    master.wait_heartbeat()
    print("Connected to flight controller.")
    return master

# Hover for a specified duration
def hover(master, duration):
    print(f"Hovering for {duration} seconds...")
    start_time = time.time()
    while time.time() - start_time < duration:
        # In GUIDED mode, the drone holds position automatically
        time.sleep(1)
        altitude = master.messages.get('GLOBAL_POSITION_INT', None)
        if altitude:
            print(f"Current altitude: {altitude.relative_alt / 1000.0} meters")
    print("Hover complete.")

# Main script
def main():
    master = connect_to_fc()
    if not master:
        return

    hover(master, 10)  # Hover for 10 seconds

    master.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()
