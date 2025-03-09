from pymavlink import mavutil
import time

# Function to connect to the flight controller
def connect_to_fc(port='/dev/ttyS0', baud=57600):
    print(f"Connecting to flight controller on {port} at {baud} baud...")
    try:
        # Establish MAVLink connection
        master = mavutil.mavlink_connection(port, baud=baud)
        # Wait for the heartbeat to confirm connection
        master.wait_heartbeat()
        print("Heartbeat received. Connected to flight controller.")
        return master
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None

# Function to attempt arming and capture pre-arm errors
def check_pre_arm(master):
    print("Attempting to arm the motors...")
    # Send arming command
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0  # 1 = arm
    )

    # Listen for STATUSTEXT messages for 10 seconds
    print("Listening for pre-arm check messages...")
    start_time = time.time()
    while time.time() - start_time < 10:
        try:
            msg = master.recv_match(type='STATUSTEXT', blocking=True, timeout=1)
            if msg:
                text = msg.text.strip()
                # Check if it's a pre-arm error
                if "PreArm" in text or "CRITICAL" in text:
                    print(f"Pre-arm check failure detected: {text}")
                else:
                    print(f"Status message: {text}")
        except KeyboardInterrupt:
            print("Stopped by user.")
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

    # Check if armed after attempt
    master.wait_heartbeat()
    if master.motors_armed():
        print("Motors successfully armed!")
    else:
        print("Motors failed to arm. Check the pre-arm errors above.")

# Main function
def main():
    # Define connection parameters (adjust as needed)
    serial_port = '/dev/ttyS0'  # Pi 3 UART port
    baud_rate = 57600          # Common baud rate for Arducopter v3.2.1

    # Connect to the flight controller
    master = connect_to_fc(serial_port, baud_rate)
    if not master:
        return

    # Check pre-arm status
    check_pre_arm(master)

    # Cleanup
    master.close()
    print("Connection closed.")

if __name__ == "__main__":
    main()