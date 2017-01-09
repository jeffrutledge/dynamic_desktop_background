# dynamic_desktop_background
Unobtrusively updates desktop background based on weather.

When run the python script `update_desktop_bg_to_weather.py` changes the file `graphics/desktop_bg.png` to represent the current weather.
It also executes the command `/usr/bin/killall Dock`, which on macOS forces the operating system to update the desktop background.
If the desktop background is set to the file `graphics/desktop_bg.png`, then this will force the system to set it to the current image.
Otherwise, macOS would just use a cache of whatever the images was when it was set as the desktop background.

The python script is periodically run using `crontab`.

<a href="https://www.wunderground.com/"> <img src="https://icons.wxug.com/logos/PNG/wundergroundLogo_4c_horz.png" width=300> </a>

Powered by Weather Underground
