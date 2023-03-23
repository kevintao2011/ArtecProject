import machine
import socket
import json
import network
f = open('config.json')
config = json.load(f)
id = config['arID']
WIFI = config['WIFI']
WIFI:dict
b = WIFI
a = {'wife':"pw"}

sta = network.WLAN(network.STA_IF)
sta.active(True)
for wife in WIFI:
    try:
        print('try connecting t WIFI:',wife)
        sta.connect(wife,b.get(wife))
        if sta.isconnected():
            break
    except:
        print('[WIFI]not found, finding next WIFI')
        
        
# # Execute the Python script on the ESP32 board
# exec(script_data, globals())