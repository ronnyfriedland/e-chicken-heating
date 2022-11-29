"""
Check if heat pad sould be turned on
"""
import datetime
import os
import argparse

import requests

from _cron import create_cron

parser = argparse.ArgumentParser(description="Job arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--latitude",
                    default=float(os.getenv('LAT', '0.0')), help="latitude")
parser.add_argument("-b", "--longitude",
                    default=float(os.getenv('LNG', '0.0')), help="longitude")
parser.add_argument(
    "-u", "--url", default=os.getenv('URL', ""), help="endpoint url")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase verbosity")
args = parser.parse_args()
config = vars(args)


HEATING_ON_FOR_SECONDS = 5 * 60 * 60
HTTP_REQUEST_TIMEOUT_SECONDS = 10


# Get today's sunrise and sunset in UTC
try:
    request_url = f"{config['url']}?lat={config['latitude']}&lon={config['longitude']}"

    if config["verbose"] is True:
        print(f"url: {request_url}".format(request_url))
        print(f"latitude: {config['latitude']}")
        print(f"longitude: {config['longitude']}")

    r = requests.get(request_url, timeout=HTTP_REQUEST_TIMEOUT_SECONDS)

    if config["verbose"] is True:
        print(f"status: {r.status_code}")

    if r.ok:
        weather_data = r.json()
        temperature = weather_data['weather']['temperature']

        if config["verbose"] is True:
            print(f"temperature: {temperature}")

        if temperature < 0:
            if config["verbose"] is True:
                print(f"temperature below 0 - turn on heating for {HEATING_ON_FOR_SECONDS}")

            # turn on the heating
            create_cron("e-chicken-heating-job", 
                        f"/usr/local/bin/python /usr/src/app/heating.py --duration {HEATING_ON_FOR_SECONDS}",
                        start=datetime.datetime.now())
        else:
            print(f"On {datetime.datetime.now()} at {config['latitude']} / {config['longitude']} the temperature was {temperature}.")
except Exception as exception:
    print(f"Error: {exception}.")
