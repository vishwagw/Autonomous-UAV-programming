# this script is for sample connecting with vehicle :
from pymavlink import mavutil

# Connect to flight controller
master = mavutil.mavlink_connection('/dev/ttyS0', baud=57600)

# Wait for heartbeat
master.wait_heartbeat()

# Arm the motors (bypassing checks if ARMING_CHECK = 0)
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0)  # 1 = arm

# Switch to AUTO mode
master.set_mode('AUTO')

# Send takeoff command
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0, 0, 0, 0, 0, 0, 0, 10)  # 10m altitude
