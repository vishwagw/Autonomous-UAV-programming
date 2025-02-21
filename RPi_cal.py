# general method of calibration without APM:
import RPi.GPIO as GPIO
import time

# for autumn: 1500Max and 900min
ESC_PIN = 18  # Change to your GPIO pin
MAX_PWM = 2000  # Max throttle (2ms pulse)
MIN_PWM = 1000  # Min throttle (1ms pulse)

GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN, GPIO.OUT)
pwm = GPIO.PWM(ESC_PIN, 50)  # 50Hz PWM (Standard for ESCs)
pwm.start(0)

def set_pwm(value):
    """Convert PWM signal to duty cycle and send to ESC."""
    duty_cycle = (value / 20000) * 100  # Convert 1000-2000μs to duty cycle
    pwm.ChangeDutyCycle(duty_cycle)

try:
    print("Starting ESC Calibration...")
    
    print("Step 1: Full throttle (Max PWM)")
    set_pwm(MAX_PWM)
    time.sleep(3)  # Wait for ESC to register max throttle

    print("Step 2: Minimum throttle (Min PWM)")
    set_pwm(MIN_PWM)
    time.sleep(3)  # Wait for ESC to register min throttle

    print("Calibration Done! Testing...")
    for i in range(5):  # Spin motor slowly for testing
        set_pwm(MIN_PWM + 200)
        time.sleep(1)
        set_pwm(MIN_PWM)
        time.sleep(1)

finally:
    print("Stopping...")
    pwm.stop()
    GPIO.cleanup()

