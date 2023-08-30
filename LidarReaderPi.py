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
        self.lidar = RPLidar(PORT_NAME)
        self.outfile = open("./LidarData/Lidar_Data " + self.localTime + '.txt', 'w')
    
    def run(self):
    
        try:
            print("lidar measuring")
            for measurment in self.lidar.iter_measurments():
                line = '\t'.join(str(v) for v in measurment)
                self.outfile.write(line + '\n')
        except KeyboardInterrupt:
            print('lidar stop')
        self.lidar.stop()
        self.lidar.disconnect()
        self.outfile.close()
            
        


# def run(path):
#     '''Main function'''
#     lidar = RPLidar(PORT_NAME)
#     outfile = open(path, 'w')
#     try:
#         print('Recording measurments... Press Crl+C to stop.')
#         for measurment in lidar.iter_measurments():
#             line = '\t'.join(str(v) for v in measurment)
#             outfile.write(line + '\n')
#     except KeyboardInterrupt:
#         print('Stoping.')
#     lidar.stop()
#     lidar.disconnect()
#     outfile.close()

# def LidarReaderPi():
#     localTime = time.strftime('%Y-%m-%d, %H-%M-%S')
#     run("./LidarData/Lidar_Data " + localTime + '.txt')