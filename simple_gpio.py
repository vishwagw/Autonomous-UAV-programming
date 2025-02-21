import RPi.GPIO as GPIO
import time

ESC_PIN = 18  # GPIO pin connected to ESC signal wire
MAX_PWM = 2000  # Max throttle (2ms pulse width)
MIN_PWM = 1000  # Min throttle (1ms pulse width)

def set_pwm(pwm):
    duty_cycle = (pwm / 20000.0) * 100  # Convert to duty cycle percentage
    pwm_signal.ChangeDutyCycle(duty_cycle)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(ESC_PIN, GPIO.OUT)

# Initialize PWM at 50Hz (standard for ESCs)
pwm_signal = GPIO.PWM(ESC_PIN, 50)
pwm_signal.start(0)

try:
    print("Starting ESC Calibration")
    print("Setting max throttle")
    set_pwm(MAX_PWM)
    time.sleep(2)  # ESCs enter calibration mode

    print("Setting min throttle")
    set_pwm(MIN_PWM)
    time.sleep(2)  # ESCs calibrate

    print("ESC Calibration Done!")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    pwm_signal.stop()
    GPIO.cleanup()
