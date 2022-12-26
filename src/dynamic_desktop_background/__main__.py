#!/usr/bin/env python3
import subprocess
import datetime
from pathlib import Path
import xdg.BaseDirectory

from . import requesters

# Commented out to remove dependencies
# def set_desktop_bg_osx(path):
#     copyfile(path, system_desktop_bg_path)
#     # Set the system desktop background image
#     desktop_bg_db_path = ('/Users/jrutledge/Library/Application Support'
#                           '/Dock/desktoppicture.db')
#     conn = sqlite3.connect(desktop_bg_db_path)
#     c = conn.cursor()
#     c.execute('UPDATE data SET value = ?', (system_desktop_bg_path, ))
#     conn.commit()
#     conn.close()
#     # Forces Mac OS to update desktop background
#     subprocess.run(['killall', 'Dock'])


def read_api_key(key_path):
    with open(key_path, 'r') as keyfile:
        key = keyfile.readline()[:-1]
    return key


def set_desktop_bg_linux(bg_path):
    print('updating background to:')
    print(bg_path)
    subprocess.run(['feh', '--bg-fill', '--no-fehbg', bg_path])


if __name__ == '__main__':
    xdg_name = 'dynamic_desktop_background'
    config_dir = Path(xdg.BaseDirectory.xdg_config_home) / xdg_name
    cache_dir = Path(xdg.BaseDirectory.xdg_cache_home) / xdg_name
    cache_dir.mkdir(parents=True, exist_ok=True)

    lat_long_cache = requesters.CachedLatLonRequester(
        api_key=read_api_key(config_dir / 'lat_lon_api_key.secret'),
        cache_path=cache_dir / 'lat_lon_cache.json',
        stale_time=datetime.timedelta(hours=1),
    )
    lat, lon = lat_long_cache.get_lat_lon()

    weather_cache = requesters.OpenWeatherRequester(
        api_key=read_api_key(config_dir / 'open_weather_api_key.secret'),
        cache_path=cache_dir / 'open_weather_cache.json',
        stale_time=datetime.timedelta(minutes=14),
        lat=lat,
        lon=lon,
    )
    bg_image_name = weather_cache.get_desktop_bg_image_name()

    desktop_bgs_dir = Path(__file__).parent / 'graphics' / 'solarized_bg_set'
    set_desktop_bg_linux(desktop_bgs_dir / bg_image_name)
