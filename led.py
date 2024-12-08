import RPi.GPIO as GPIO
import time

LED_PIN = 17
UNIT = 0.25  # One unit = 0.25 seconds

# Morse code dictionary
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', ' ': ' ',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)

def activate_led():
    GPIO.output(LED_PIN, GPIO.HIGH)

def deactivate_led():
    GPIO.output(LED_PIN, GPIO.LOW)

def dot():
    activate_led()
    time.sleep(UNIT)
    deactivate_led()
    time.sleep(UNIT)  # Space between parts of same letter

def dash():
    activate_led()
    time.sleep(UNIT * 3)
    deactivate_led()
    time.sleep(UNIT)  # Space between parts of same letter

def transmit_letter(letter):
    if letter == ' ':
        time.sleep(UNIT * 7)  # Space between words
        return
        
    morse = MORSE_CODE[letter.upper()]
    for symbol in morse:
        if symbol == '.':
            dot()
        elif symbol == '-':
            dash()
    
    time.sleep(UNIT * 2)  # Additional 2 units for letter spacing (1 unit already added after dot/dash)

def transmit_message(message):
    for char in message:
        if char.upper() in MORSE_CODE:
            transmit_letter(char)

def main():
    try:
        setup()
        while True:
            message = input("Enter message to transmit (or Ctrl+C to exit): ")
            transmit_message(message)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
