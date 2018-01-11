#!/usr/bin/env python3
import json
import os
from os import path
import requests
import subprocess
import sys

RELATIVE_WEATHER_JSON_PATH = 'weather.json'
RELATIVE_WUNDERGROUND_API_KEY_PATH = 'wunderground_api_key.private'
RELATIVE_SYSTEM_DESKTOP_BG_PATH = 'graphics/desktop_bg.png'
RELATIVE_DESKTOP_BGS_DIR = 'graphics/solarized_bg_set'
DESKTOP_BG_NAME_FROM_ICON = {
    'chanceflurries': 'snow.png',
    'chancerain': 'rain.png',
    'chancesleet': 'snow.png',
    'chancesnow': 'snow.png',
    'chancetstorms': 'rain.png',
    'clear': 'clear.png',
    'cloudy': 'full_clouds.png',
    'flurries': 'snow.png',
    'fog': 'clear.png',
    'hazy': 'clear.png',
    'mostlycloudy': 'partly_cloudy.png',
    'mostlysunny': 'partly_sunny.png',
    'partlycloudy': 'partly_cloudy.png',
    'partlysunny': 'partly_sunny.png',
    'rain': 'rain.png',
    'sleet': 'sleet.png',
    'snow': 'snow.png',
    'sunny': 'sun.png',
    'tstorms': 'rain.png'
}


def get_wunderground_api_key():
    with open(wunderground_api_key_path, 'r') as keyfile:
        key = keyfile.readline()[:-1]
    return key


def update_weather():
    url_base = 'http://api.wunderground.com/api'
    url_params = 'conditions/q/autoip.json'
    request_url = '/'.join((url_base, get_wunderground_api_key(), url_params))
    weather_request = requests.get(request_url).json()

    with open(weather_json_path, 'w') as outfile:
        json.dump(weather_request, outfile)

    return weather_request


def get_stored_weather():
    with open(weather_json_path, 'r') as infile:
        request_json = json.load(infile)

    return request_json


def get_desktop_bg_path(weather=None):
    if not weather:
        weather = get_stored_weather()

    icon = weather['current_observation']['icon']
    desktop_bg_name = DESKTOP_BG_NAME_FROM_ICON[icon]
    return path.join(desktop_bgs_dir, desktop_bg_name)


# Commented out to remove dependencies
# def set_desktop_bg_osx(path):
#     copyfile(path, system_desktop_bg_path)
#     # Set the system desktop background image
#     desktop_bg_db_path = ('/Users/jrutledge/Library/Application Support/Dock/'
#                           'desktoppicture.db')
#     conn = sqlite3.connect(desktop_bg_db_path)
#     c = conn.cursor()
#     c.execute('UPDATE data SET value = ?', (system_desktop_bg_path, ))
#     conn.commit()
#     conn.close()
#     # Forces Mac OS to update desktop background
#     subprocess.run(['killall', 'Dock'])


def set_desktop_bg_linux(bg_path):
    print('updating background to:')
    print(bg_path)

    subprocess.run(['feh', '--bg-fill', '--no-fehbg', bg_path])


if __name__ == '__main__':
    file_path = os.path.abspath(os.path.dirname(__file__))
    weather_json_path = path.join(file_path, RELATIVE_WEATHER_JSON_PATH)
    system_desktop_bg_path = path.join(file_path,
                                       RELATIVE_SYSTEM_DESKTOP_BG_PATH)
    desktop_bgs_dir = path.join(file_path, RELATIVE_DESKTOP_BGS_DIR)
    wunderground_api_key_path = path.join(
            file_path, RELATIVE_WUNDERGROUND_API_KEY_PATH)

    try:
        weather = update_weather()
    except requests.exceptions.ConnectionError:
        print('Unable to establish connection to WunderGround weather api.',
              file=sys.stderr)
        sys.exit(1)

    set_desktop_bg_linux(get_desktop_bg_path(weather))
