# boot.py -- run on boot-up
import json
f = open('config.json')
config = json.load(f)
id = config['arID']

print("[boot]]Running boot script from Robot ",id)
from utime import sleep_ms