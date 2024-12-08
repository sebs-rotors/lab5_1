import RPi.GPIO as GPIO
import time

LED_PIN = 17

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

def activate_led():
    GPIO.output(LED_PIN, GPIO.HIGH)

def deactivate_led():
    GPIO.output(LED_PIN, GPIO.LOW)

def main():
    try:
        setup()
        while True:
            activate_led()
            time.sleep(5)
            deactivate_led() 
            time.sleep(3)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
