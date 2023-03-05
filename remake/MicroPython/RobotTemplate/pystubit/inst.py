"""
Button
"""
from .button import StuduinoBitButton
button_a = StuduinoBitButton('A')
button_b = StuduinoBitButton('B')

"""
Image
"""
from .image import StuduinoBitImage as Image

"""
Display
"""
from .dsply import StuduinoBitDisplay
display = StuduinoBitDisplay()

"""
Terminal
"""
from .terminal import StuduinoBitTerminal, StuduinoBitTerminalForMB
p0 = StuduinoBitTerminal('P0')
p1 = StuduinoBitTerminal('P1')
p2 = StuduinoBitTerminal('P2')
p3 = StuduinoBitTerminal('P3')
p4 = StuduinoBitTerminal('P4')
p5 = StuduinoBitTerminal('P5')
p6 = StuduinoBitTerminal('P6')
p7 = StuduinoBitTerminal('P7')
p8 = StuduinoBitTerminal('P8')
p9 = StuduinoBitTerminal('P9')
p10 = StuduinoBitTerminal('P10')
p11 = StuduinoBitTerminal('P11')
p12 = StuduinoBitTerminal('P12')
p13 = StuduinoBitTerminal('P13')
p14 = StuduinoBitTerminal('P14')
p15 = StuduinoBitTerminal('P15')
p16 = StuduinoBitTerminal('P16')
p19 = StuduinoBitTerminal('P19')
p20 = StuduinoBitTerminal('P20')

pin0 = StuduinoBitTerminalForMB('P0')
pin1 = StuduinoBitTerminalForMB('P1')
pin2 = StuduinoBitTerminalForMB('P2')
pin3 = StuduinoBitTerminalForMB('P3')

"""
Bus
"""
from .bus import StuduinoBitI2C, StuduinoBitSPI
i2c = StuduinoBitI2C()
i2c.init()
spi = StuduinoBitSPI()


"""
Sensor
"""
from .sensor import StuduinoBitLightSensor, \
                    StuduinoBitTemperature, \
                    StuduinoBitAccelerometer, \
                    StuduinoBitGyro, \
                    StuduinoBitCompass

lightsensor = StuduinoBitLightSensor()
temperature = StuduinoBitTemperature()
accelerometer = StuduinoBitAccelerometer()
gyro = StuduinoBitGyro()
compass = StuduinoBitCompass()

"""
Circuit
"""
from .circuit import StuduinoBitUART
uart = StuduinoBitUART()

"""
Buzzer
"""
from .bzr import StuduinoBitBuzzer
buzzer = StuduinoBitBuzzer()

"""
Network
"""
from .nw import CreateWLAN



