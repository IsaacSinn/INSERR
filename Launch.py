# TODO: Change serial bandwidth for CAN-USB, 


import time
from ModuleBase import ModuleManager
from PyGameServices import PyGameServices

# MODULES
from GUI import GUI
from Joystick import Joystick
from ControlProfile import ControlProfile
from ThrusterPower import ThrusterPower
from Thrusters import Thrusters
from CANHandler import CANHandler
from Logger import Logger
from EthernetServer import EthernetClientHandler

mm = ModuleManager()
pygs = PyGameServices()
pygs.start(100)

GUI_FPS = 60

GUI = GUI()
Joystick = Joystick()
ControlProfileA = ControlProfile(100, 30, "A")
ControlProfileB = ControlProfile(70, 50, "B")
ControlProfileC = ControlProfile(50, 50, "C")
ControlProfileD = ControlProfile(30, 50, "D")
ThrusterPower = ThrusterPower()
Thrusters = Thrusters()
EthernetClientHandler = EthernetClientHandler()
# CANHandler = CANHandler(115200) # BAUDRATE
Logger = Logger(False, False, None, "ethernet.send") # FILE, PRINT, RATE_LIMITER, TOPICS

# REGISTERING MODULES (INSTANCE, REFRESH PER SECOND)
mm.register(
            (GUI, GUI_FPS),
            (Joystick, 60),
            (ControlProfileA, 1),
            (ControlProfileB, 1),
            (ControlProfileC, 1),
            (ControlProfileD, 1),
            (ThrusterPower, 60),
            (Thrusters, 1),
            (EthernetClientHandler, 1)
            # (CANHandler, 1),
)

mm.start_all()

try:
    while True:
        pygs.get_pygame().event.get()
        pygs.get_pygame().time.delay((2)) # ms
except KeyboardInterrupt:
    mm.stop_all()