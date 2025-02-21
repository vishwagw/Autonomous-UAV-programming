from dronekit import connect, VehicleMode
import time

# Connect to the flight controller (adjust the port if using UART)
autumn1 = connect('/dev/ttyACM0', baud=115200, wait_ready=True)
# For USB connection, use: vehicle = connect('/dev/ttyUSB0', baud=115200, wait_ready=True)

def calibrate_escs():
    print("Starting ESC Calibration...")

    # Step 1: Set mode to 'STABILIZE' (required for manual throttle control)
    autumn1.mode = VehicleMode("STABILIZE")
    time.sleep(2)

    # Step 2: Arm the vehicle (bypass safety checks for calibration)
    autumn1.armed = True
    while not autumn1.armed:
        print("Waiting for vehicle to arm...")
        time.sleep(1)
    
    print("Vehicle armed. Applying maximum throttle for calibration.")

    # Step 3: Send maximum throttle signal
    autumn1.channels.overrides['3'] = 2000  # Throttle channel (CH3)
    time.sleep(3)  # Allow ESCs to enter calibration mode (listen for beeps)

    print("Now setting throttle to minimum.")
    # Step 4: Send minimum throttle signal
    autumn1.channels.overrides['3'] = 1000
    time.sleep(5)  # ESCs should beep to confirm calibration

    # Step 5: Disarm the vehicle and clear overrides
    autumn1.armed = False
    autumn1.channels.overrides = {}

    print("ESC Calibration Complete.")

try:
    calibrate_escs()
finally:
    autumn1.close()


