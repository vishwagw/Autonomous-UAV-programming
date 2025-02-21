from dronekit import connect, VehicleMode
import time

# Connect to the flight controller (adjust the port if using UART)
autumn1 = connect('/dev/ttyACM0', baud=115200, wait_ready=True)
# For USB connection, use: vehicle = connect('/dev/ttyUSB0', baud=115200, wait_ready=True)

# Disable arming checks
autumn1.parameters['ARMING_CHECK'] = 0
# alternative:
autumn1.parameters['GPS_HDOP_GOOD'] = 9999

# Enter MANUAL mode (or STABILIZE)
autumn1.mode = VehicleMode("STABILIZE")
while not autumn1.mode.name == 'STABILIZE':
    print("Waiting for mode change...")
    time.sleep(1)

# Arm the vehicle
autumn1.armed = True
while not autumn1.armed:
    print("Waiting for arming...")
    time.sleep(1)

# Set throttle to max for calibration
print("Sending max throttle for calibration...")
autumn1.channels.overrides['3'] = 2000  # Channel 3 is throttle
time.sleep(5)  # Wait for ESCs to register max throttle

# Lower throttle to minimum
print("Setting throttle to minimum...")
autumn1.channels.overrides['3'] = 1000
time.sleep(5)  # Allow ESCs to complete calibration

# Clear overrides
autumn1.channels.overrides = {}

# Disarm the vehicle
autumn1.armed = False

# Close connection
autumn1.close()
print("ESC Calibration Completed!")

