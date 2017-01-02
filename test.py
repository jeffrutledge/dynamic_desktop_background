from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import subprocess
import requests
from requests.compat import urljoin
import json

def get_wunderground_api_key():
    with open('./wunderground_api_key.private', 'r') as keyfile:
        key = keyfile.readline()[:-1]
    return key

def get_location():
    request_url = 'http://geoip.nekudo.com/api//en/short'
    location_json = requests.get(request_url).json()

    with open('location.json', 'w') as location_file:
        json.dump(location_json, location_file)

def load_location():
    with open('location.json', 'r') as location_file:
        location = json.load(location_file)['location']
    return location

def save_request(file_name, request_url):
    request_json = requests.get(request_url).json()

    print(request_json)

    with open(file_name, 'w') as outfile:
        json.dump(outfile, file_name)

def load_request(file_name):
    with open(file_name, 'r') as infile:
        request_json = json.load(infile)

    return request_json

def get_weather():
    url_base = 'http://api.wunderground.com/api'
    url_params = 'conditions/q/autoip.json'
    request_url = '/'.join((url_base, get_wunderground_api_key(), url_params))
    weather_request = requests.get(request_url).json()

    with open('weather.json', 'w') as outfile:
        json.dump(weather_request, outfile)

def update_desktop_bg(temp):
    desktop_bg = Image.open('./graphics/meditating_person_light_white_bg.png')
    part_cloud = Image.open('./graphics/part_cloud.png')
    size = tuple(x // 4 for x in part_cloud.size)
    # desktop_bg.paste(part_cloud.resize(size), (0, 0, 0 + size[0], 0 + size[1]))
    
    draw = ImageDraw.Draw(desktop_bg)
    font = ImageFont.truetype('/System/Library/Fonts/Avenir.ttc', 35)
    text = u'{:2.0f}°F'.format(temp)
    text_size = draw.textsize(text, font=font)
    draw.text((640 - text_size[0] / 2, 310 - text_size[1] / 2), text, (255, 255, 255), font=font)
    desktop_bg.save('./graphics/desktop_bg.png')

    # Forces Mac OS to update desktop background
    subprocess.run(['/usr/bin/killall', 'Dock'])

weather = load_request('weather.json')
temp = weather['current_observation']['temp_f']
update_desktop_bg(temp)
