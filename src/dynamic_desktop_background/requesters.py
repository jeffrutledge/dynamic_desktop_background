import json
import datetime
from pathlib import Path
from abc import ABC, abstractmethod

import requests


class CachedRequester(ABC):
    def __init__(self, api_key, cache_path, stale_time):
        self._api_key = api_key
        self._cache_path = Path(cache_path)
        self.stale_time = stale_time

    def cache_age(self, cache):
        cache_time = datetime.datetime.fromisoformat(cache['update_dt_iso'])
        return datetime.datetime.utcnow() - cache_time

    def get_cache(self):
        if not self._cache_path.exists():
            return None

        with open(self._cache_path, 'r') as cache:
            return json.load(cache)

    def set_cache(self, data):
        cache_dict = dict(
            update_dt_iso=datetime.datetime.utcnow().isoformat(),
            data=data,
        )
        with open(self._cache_path, 'w') as cache_file:
            json.dump(cache_dict, cache_file)

    @abstractmethod
    def _request(self):
        pass

    def get(self):
        cache = self.get_cache()
        if cache:
            print(f'cache_age={self.cache_age(cache)}'
                  f' stale_time={self.stale_time}')

        if cache and self.cache_age(cache) < self.stale_time:
            print('Using cached data.')
            return cache['data']
        else:
            print('Cache is stale, requesting update.')
            data = self._request()
            self.set_cache(data)
            return data


class CachedLatLonRequester(CachedRequester):
    def _request(self):
        url_base = 'http://api.ipapi.com/check'
        url_params = dict(
            access_key=self._api_key,
        )
        weather_json = requests.get(url_base, params=url_params).json()
        return weather_json

    def get_lat_lon(self):
        data = self.get()
        return data['latitude'], data['longitude']


class CachedWeatherRequester(CachedRequester):
    @classmethod
    @abstractmethod
    def _weather_to_desktop_bg_image_name(cls, weather):
        pass

    def get_desktop_bg_image_name(self):
        weather = self.get()
        return self._weather_to_desktop_bg_image_name(weather)


class OpenWeatherRequester(CachedWeatherRequester):
    def __init__(self, *args, lat, lon, **kwargs):
        super().__init__(*args, **kwargs)
        self._lat = lat
        self._lon = lon

    @classmethod
    def _weather_to_desktop_bg_image_name(cls, weather):
        """
        See: https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
        """
        weather_id = weather['weather'][0]['id']

        def w_in(x, y=None):
            return x <= weather_id and weather_id < y

        if w_in(200, 300) or w_in(300, 400) or w_in(500, 600):
            return 'rain.png'
        elif w_in(600, 700):
            return 'snow.png'
        elif w_in(800, 900):
            if w_in(800, 801):
                return 'sun.png'
                return 'clear.png'
            elif w_in(801, 802):
                return 'partly_sunny.png'
            elif w_in(802, 804):
                return 'partly_cloudy.png'
            elif w_in(804, 805):
                return 'full_clouds.png'

        return 'clear.png'

    def _request(self):
        url_base = 'https://api.openweathermap.org/data/2.5/weather'
        url_params = dict(
            lat=self._lat,
            lon=self._lon,
            appid=self._api_key,
        )
        weather_request = requests.get(url_base, params=url_params)
        weather_json = weather_request.json()
        return weather_json


class WundergroundWeatherRequester(CachedWeatherRequester):
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
        'mostlycloudy': 'full_clouds.png',
        'mostlysunny': 'partly_sunny.png',
        'partlycloudy': 'partly_cloudy.png',
        'partlysunny': 'partly_sunny.png',
        'rain': 'rain.png',
        'sleet': 'sleet.png',
        'snow': 'snow.png',
        'sunny': 'sun.png',
        'tstorms': 'rain.png'
    }

    @classmethod
    def _weather_to_desktop_bg_image_name(cls, weather):
        icon = weather['current_observation']['icon']
        return cls.DESKTOP_BG_NAME_FROM_ICON[icon]

    def _request_weather(self):
        url_base = 'http://api.wunderground.com/api'
        url_params = 'conditions/q/autoip.json'
        request_url = '/'.join((url_base,
                                self._api_key,
                                url_params))
        weather_json = requests.get(request_url).json()

        with open(weather_json_path, 'w') as outfile:
            json.dump(weather_json, outfile)

        return weather_json
