import sys
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
from EthernetServer import EthernetHandler
import os

# allow pygame to not be in focus and still works
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

mm = ModuleManager()
pygs = PyGameServices()
pygs.start(100)

GUI = GUI()
Joystick = Joystick()
ControlProfileA = ControlProfile(100, 30, "A")
ControlProfileB = ControlProfile(70, 50, "B")
ControlProfileC = ControlProfile(50, 50, "C")
ControlProfileD = ControlProfile(30, 50, "D")
ThrusterPower = ThrusterPower()
Thrusters = Thrusters()
EthernetHandler = EthernetHandler()
# CANHandler = CANHandler(115200) # BAUDRATE
Logger = Logger(False, False, None, "ethernet.send") # FILE, PRINT, RATE_LIMITER, TOPICS
    
# REGISTERING MODULES (INSTANCE, REFRESH PER SECOND)
mm.register(
            (GUI, 60),
            (Joystick, 60),
            (ControlProfileA, 1),
            (ControlProfileB, 1),
            (ControlProfileC, 1),
            (ControlProfileD, 1),
            (ThrusterPower, 60),
            (Thrusters, 3),
            (EthernetHandler, 120)
            # (CANHandler, 1),
)

try:
    mm.start_all()
    pygame = pygs.get_pygame()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
except KeyboardInterrupt:
    pygame.display.quit()
    pygame.quit()
    mm.stop_all()
    print("stopped all modules")
    sys.exit()
finally:
    pygame.display.quit()
    pygame.quit()
    mm.stop_all()
    #TODO: stuck at stopping ethernet client handler, blocking call socket.accept() 
    print("stopped all modules")
    sys.exit()