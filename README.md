# dynamic_desktop_background
Updates desktop background based on weather.

## Usage
1. Add api keys to `~/.config/dynamic_desktop_background` (or whatever XDG config dir is set)
    1. `lat_long_api_key.secret`: [ipapi](https://ipapi.com)
    2. `open_weather_api_key.secret`: [open weather](https://openweathermap.org)
2. Add module to `PYTHONPATH`
3. Setup a periodic job to run `python3 -m dynamic_desktop_background`
    1. could use either `crontab` or `systemd` service
    2. [systemd service example](https://github.com/jeffrutledge/dotfiles/tree/master/dynamic_desktop_background/.config/systemd/user)

### Dependencies
- `requests` 
- `feh`: for updating background
