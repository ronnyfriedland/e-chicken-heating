"""
Control gpio
"""
import time
import argparse

from RPi import GPIO

GPIO.setmode(GPIO.BCM)

parser = argparse.ArgumentParser(description="Job arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", "--pin", default=6, help="gpio relais pin")
parser.add_argument("-d", "--duration", default=0, help="relais on duration in seconds")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()
config = vars(args)

try:
    if config["verbose"] is True:
        print(f"pin: {config['pin']}")
        print(f"duration: {config['duration']}")

    GPIO.setup(int(config["pin"]), GPIO.OUT)

    if config["verbose"] is True:
        print("set pin to HIGH")
    GPIO.output(int(config["pin"]), GPIO.HIGH)

    time.sleep(int(config["duration"]))

    if config["verbose"] is True:
        print("set pin to LOW")
    GPIO.output(int(config["pin"]), GPIO.LOW)
finally:
    GPIO.cleanup()
