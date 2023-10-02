# Ultra Results

This repository contains Python scripts for web scraping select ultramarathon race results. Please limit requests.

## Western States Endurance Run (WSER)

`wser.py` downloads all [WSER race results](https://www.wser.org/results/) from 1974 to present. Future canceled races must be added to NO_RESULT_RACES. The WSER website DOM hasn't been updated since at least 2012[^1] so this script will hopefully work for some time.

[^1]: [Wayback Machine](https://web.archive.org/web/20121206023353/https://www.wser.org/results/)