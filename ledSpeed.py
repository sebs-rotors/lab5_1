#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import sys

LED_PIN = 17
UNIT = 0.014  # One unit = 0.050 seconds

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
    time.sleep(UNIT * 1.98)
    deactivate_led()
    time.sleep(UNIT)  # Space between parts of same letter

def transmit_letter(letter):
    if letter == ' ':
        time.sleep(UNIT * 1.28)  # Space between words
        return
        
    morse = MORSE_CODE[letter.upper()]
    for symbol in morse:
        if symbol == '.':
            dot()
        elif symbol == '-':
            dash()

def transmit_message(message):
    for char in message:
        if char.upper() in MORSE_CODE:
            transmit_letter(char)
            time.sleep(UNIT * 1.28)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./led <repeat_count> <message>")
        sys.exit(1)
        
    try:
        repeat_count = int(sys.argv[1])
        message = sys.argv[2]
        
        setup()
        for _ in range(repeat_count):
            transmit_message(message)
            time.sleep(UNIT * 11.52)  # Pause between message repetitions
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nProgram terminated by user")
    except ValueError:
        print("Error: First argument must be a number")
        GPIO.cleanup()
    except Exception as e:
        print(f"An error occurred: {e}")
        GPIO.cleanup()

if __name__ == "__main__":
    main()
