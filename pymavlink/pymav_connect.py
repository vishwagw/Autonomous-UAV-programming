# this is a test program to use pyavlink to connect the vehicle:
from pymavlink import mavutil

master = mavutil.mavlink_connection('/dev/ttyS0', baud=57600)
master.wait_heartbeat()
master.mav.command_long_send(master.target_system, master.target_component,
                             mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
                             0, 1, 0, 0, 0, 0, 0, 0)
master.set_mode('AUTO')
master.mav.command_long_send(master.target_system, master.target_component,
                             mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
                             0, 0, 0, 0, 0, 0, 0, 10)  # 10m
