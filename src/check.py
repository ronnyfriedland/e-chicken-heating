import datetime
import os
import argparse

import requests

from _cron import *

parser = argparse.ArgumentParser(description="Job arguments",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--latitude", default=float(os.getenv('LAT', 0.0)), help="latitude")
parser.add_argument("-b", "--longitude", default=float(os.getenv('LNG', 0.0)), help="longitude")
parser.add_argument("-u", "--url", default=os.getenv('URL', ""), help="endpoint url")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()
config = vars(args)


now = datetime.datetime.now()
heating_on_for_seconds = 7200


# Get today's sunrise and sunset in UTC
try:
    request_url = "{}?lat={}&lon={}".format(config['url'], config['latitude'], config['longitude'])

    if config["verbose"] is True:
        print("url: {}".format(request_url))
        print("latitude: {}".format(config["latitude"]))
        print("longitude: {}".format(config["longitude"]))

    r = requests.get(request_url)

    if config["verbose"] is True:
        print("status: {}".format(r.status_code))

    if r.ok:
        weather_data = r.json()
        temperature = weather_data['weather']['temperature']

        if config["verbose"] is True:
            print("temperature: {}".format(temperature))


        if temperature < 0:
            if config["verbose"] is True:
                print("temperature below 0 - turn on heating for {}".format(heating_on_for_seconds))

            # turn on the heating
            create_cron("e-chicken-heating-job", "/usr/local/bin/python /usr/src/app/heating.py --duration {duration}".format(duration = heating_on_for_seconds), start=now)
        else:
          print('On {} at {} / {} the temperature was {}.'.
              format(now, config["latitude"], config["longitude"], temperature))
except Exception as e:
    print("Error: {}.".format(e))
