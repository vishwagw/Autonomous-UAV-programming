from dronekit import connect, VehicleMode
import time

# Connect to the vehicle
vehicle = connect('/dev/serial0', baud=57600, wait_ready=True)

def set_rc_channel_pwm(channel, pwm):
    """ Set RC channel PWM value. Channel 3 is usually throttle. """
    if channel < 1 or channel > 18:
        print("Invalid channel")
        return

    # Create a dictionary to override RC channels
    #overrides = vehicle.channels
    #overrides[channel] = pwm
    vehicle.channels.overrides = {channel: pwm}
    print(f"Set Channel {channel} to {pwm}")

try:
    print("Starting ESC Calibration")

    # Put ESCs in calibration mode (full throttle)
    set_rc_channel_pwm(3, 2000)
    time.sleep(3)

    # Lower throttle to calibrate
    set_rc_channel_pwm(3, 1000)
    time.sleep(3)

    print("ESC Calibration Done!")

finally:
    # Clear RC override
    vehicle.channels.overrides = {}
    vehicle.close()
