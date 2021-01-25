from abc import ABC, abstractmethod
import json

class CachedWeatherRequester(ABC):
    @staticmethod
    @abstractmethod
    def _weather_to_desktop_bg_image_name():
        pass

    def __init__(self, api_key, cache_path, stale_time):
        self._api_key = api_key
        self._cache_path = cache_path
        self.stale_time = stale_time

    @abstractmethod
    def cache_age(self):
        pass

    def get_cached_weather(self):
        with open(self._cache_path, 'r') as cache:
            return json.load(cache)

    def set_cached_weather(self, weather):
        with open(weather_json_path, 'w') as outfile:
            json.dump(weather, self._cache_path)

    @abstractmethod
    def _request_weather(self):
        pass

    def get_weather(self):
        if self.cache_age() < self.stale_time:
            return self.get_cached_weather()
        else:
            weather = self._request_weather()
            self.set_cached_weather(weather)
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
    def _weather_to_desktop_bg_image_name(weather):
        pass

    def cache_age(self):
        with open(weather_json_path, 'r') as infile:
            weather_json = json.load(infile)
        # Check if json file is cached observation
        if 'current_observation' in weather_json:
            # Check if stale
            last_update_time_str = weather_json['current_observation'][
                'local_time_rfc822']
            last_update_time = datetime.datetime.strptime(
                last_update_time_str, '%a, %d %b %Y %H:%M:%S %z')
            # Remove timezone, because datetime.now has no timezone
            last_update_time = last_update_time.replace(tzinfo=None)
            need_to_update_weather = (datetime.datetime.now() -
                                      last_update_time > stale_time)

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
