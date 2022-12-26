import json
import datetime
from pathlib import Path
from abc import ABC, abstractmethod


class CachedWeatherRequester(ABC):
    @classmethod
    @abstractmethod
    def _weather_to_desktop_bg_image_name(cls, weather):
        pass

    def __init__(self, api_key, cache_path, stale_time):
        self._api_key = api_key
        self._cache_path = Path(cache_path)
        self.stale_time = stale_time

    def cache_age(self, cache):
        cache_time = datetime.datetime.fromisoformat(cache['update_dt_iso'])
        return datetime.datetime.utcnow() - cache_time

    def get_cache(self):
        with open(self._cache_path, 'r') as cache:
            return json.load(cache)

    def set_cache(self, weather):
        cache_dict = dict(
            update_dt_iso=datetime.datetime.isoformat(),
            weather=weather,
        )
        with open(self._cache_path, 'w') as cache_file:
            json.dump(cache_dict, cache_file)

    @abstractmethod
    def _request_weather(self):
        pass

    def get_weather(self):
        print('Getting weather.')
        cache = self.get_cache()
        cache_age = self.cache_age(cache)
        print(f'cache_age={cache_age} stale_time={self.stale_time}')
        if cache_age < self.stale_time:
            print('Using cached weather.')
            return cache['weather']
        else:
            print('Cache is stale, requesting update.')
            weather = self._request_weather()
            self.set_cache(weather)
            return weather

    def get_current_desktop_bg_image_name(self):
        weather = self.get_weather()
        return self._weather_to_desktop_bg_image_name(weather)


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
