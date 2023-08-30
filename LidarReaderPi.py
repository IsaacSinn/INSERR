#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:

$ ./record_measurments.py out.txt'''
from rplidar import RPLidar
import time
from ModuleBase import Module


PORT_NAME = '/dev/ttyUSB0'

class LidarReaderPi(Module):
    def __init__(self):
        super.__init__()

        self.localtime = time.strftime('%Y-%m-%d, %H-%M-%S')
        try:
            self.lidar = RPLidar(PORT_NAME)
        except:
            print("Lidar port incorrect")
        self.outfile = open("./LidarData/Lidar_Data " + self.localTime + '.txt', 'w')
    
    def run(self):
    
        try:
            print("lidar measuring")
            for measurment in self.lidar.iter_measurments():
                line = '\t'.join(str(v) for v in measurment)
                self.outfile.write(line + "\t" + str(time.time()) + '\n')
        except KeyboardInterrupt:
            print('lidar stop')
        self.lidar.stop()
        self.lidar.disconnect()
        self.outfile.close()
            
        