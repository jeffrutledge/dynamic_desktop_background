# dynamic_desktop_background
Updates desktop background based on weather.

## Usage

1. Add module to `PYTHONPATH` and run
2. Add api key to `~/.config/dynamic_desktop_background/api_key.secret`.
3. run `python3 -m dynamic_desktop_background`

### Dependencies
- `feh` for updating background

### Example
This can be run periodically using a systemd service or crontab.
```
