from dronekit import connect, VehicleMode
import time

# Connect to the flight controller (adjust the port if using UART)
autumn1 = connect('/dev/ttyACM0', baud=115200, wait_ready=True)
# For USB connection, use: vehicle = connect('/dev/ttyUSB0', baud=115200, wait_ready=True)

# function:
def cal_esc():
    print("Starting ESC Calibration...")

    # Step 1: Disarm the drone
    autumn1.armed = False
    time.sleep(2)

    # Step 2: Set flight mode to 'STABILIZE' (required for some setups)
    autumn1.mode = VehicleMode("STABILIZE")
    time.sleep(2)

    # Step 3: Enter ESC calibration mode
    print("Entering ESC calibration mode...")
    autumn1.parameters['ARMING_CHECK'] = 0  # Disable arming checks
    autumn1.armed = True
    time.sleep(2)

     # Step 4: Send maximum throttle (this triggers ESC calibration mode)
    print("Sending MAX throttle for calibration...")
    autumn1.channels.overrides['3'] = 2000  # Throttle max
    time.sleep(5)  # Wait for ESC beeps

    # Step 5: Send minimum throttle to save calibration
    print("Sending MIN throttle to finalize calibration...")
    autumn1.channels.overrides['3'] = 1000  # Throttle min
    time.sleep(5)

    # Step 6: Reset everything
    autumn1.channels.overrides = {}
    autumn1.armed = False
    autumn1.parameters['ARMING_CHECK'] = 1  # Re-enable arming checks

    print("ESC calibration complete.")

# excute the calibration:
cal_esc()

