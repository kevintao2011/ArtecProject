# main.py
print('-------start main script-------')
from pyatcrobo2.parts import DCMotor
L = DCMotor('M1')
R = DCMotor('M2')
from pystubit.button import StuduinoBitButton
button_a = StuduinoBitButton('A')
button_b = StuduinoBitButton('B')
from pystubit.sensor import StuduinoBitCompass
# compass = StuduinoBitCompass ()
# compassReading = compass.heading()
# if(button_b.is_pressed):
#     compass.calibrate()

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('NETGEAR76', 'quiettulip014')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
do_connect()
def connectServer():
    import socket
    ADDR = ('192.168.1.83', 6000) 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)