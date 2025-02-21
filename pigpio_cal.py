import pigpio
import time

ESC_PIN = 18  # GPIO pin connected to ESC signal wire
pi = pigpio.pi()

# for autumn: 1500 max and 900min
MAX_PWM = 2000  # 2ms (Full throttle)
MIN_PWM = 1000  # 1ms (Zero throttle)

print("Starting ESC Calibration...")

# Step 1: Full throttle
pi.set_servo_pulsewidth(ESC_PIN, MAX_PWM)
time.sleep(3)

# Step 2: Minimum throttle
pi.set_servo_pulsewidth(ESC_PIN, MIN_PWM)
time.sleep(3)

print("Calibration Done! Testing...")
for i in range(5):
    pi.set_servo_pulsewidth(ESC_PIN, MIN_PWM + 200)  # Slightly above minimum
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC_PIN, MIN_PWM)  # Idle
    time.sleep(1)

# Cleanup
pi.set_servo_pulsewidth(ESC_PIN, 0)
pi.stop()
