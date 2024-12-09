#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import sys

LED_PIN = 17
UNIT = 0.01  # One unit = 0.008 seconds

# Morse code dictionary - using tuples for slightly better performance
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

# Pre-calculate common time intervals
DOT_TIME = UNIT
DASH_TIME = UNIT * 3.6
LETTER_SPACE = UNIT * 2.4
MESSAGE_SPACE = UNIT * 21.6

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_PIN, GPIO.OUT)
    return GPIO.output

def dot(output_func):
    output_func(LED_PIN, GPIO.HIGH)
    time.sleep(DOT_TIME)
    output_func(LED_PIN, GPIO.LOW)
    time.sleep(UNIT)

def dash(output_func):
    output_func(LED_PIN, GPIO.HIGH)
    time.sleep(DASH_TIME)
    output_func(LED_PIN, GPIO.LOW)
    time.sleep(UNIT)

def transmit_letter(letter, output_func):
    if letter == ' ':
        time.sleep(LETTER_SPACE)
        return
        
    morse = MORSE_CODE[letter.upper()]
    for symbol in morse:
        if symbol == '.':
            dot(output_func)
        else:
            dash(output_func)

def transmit_message(message, output_func):
    for char in message:
        if char.upper() in MORSE_CODE:
            transmit_letter(char, output_func)
            time.sleep(LETTER_SPACE)

def main():
    if len(sys.argv) != 3:
        print("Usage: ./led <repeat_count> <message>")
        sys.exit(1)
        
    try:
        repeat_count = int(sys.argv[1])
        message = sys.argv[2]
        
        output_func = setup()
        for _ in range(repeat_count):
            transmit_message(message, output_func)
            time.sleep(MESSAGE_SPACE)
            
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
