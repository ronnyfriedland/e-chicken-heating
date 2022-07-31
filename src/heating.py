import RPi.GPIO as GPIO
import time
import argparse

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
        print("pin: {}".format(config["pin"]))
        print("duration: {}".format(config["duration"]))

    GPIO.setup(config["pin"], GPIO.OUT) # GPIO Modus zuweisen

    if config["verbose"] is True:
        print("set pin to HIGH")
    GPIO.output(config["pin"], GPIO.HIGH) # an

    time.sleep(config["duration"])

    if config["verbose"] is True:
        print("set pin to LOW")
    GPIO.output(config["pin"], GPIO.LOW) # aus
finally:
    GPIO.cleanup()
