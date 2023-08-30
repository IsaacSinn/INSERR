# echo-client.py
import time
import socket
import struct
from pubsub import pub
from ModuleBase import Module

class EthernetClient(Module):
    def __init__(self):
        super().__init__()

        self.HOST = "169.254.196.165"  # The server's hostname or IP address
        self.PORT = 50001  # The port used by the server

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))

        print(f"Connected to server {self.HOST}")

        pub.subscribe(self.message_listener, "ethernet.send")
    
    def message_listener(self, message):

        if message["type"] == "CAN":

            START = "X".encode()
            message_type = "CAN".encode()

            address1 = message["address"] >> 8 & 0xff
            address2 = message["address"] & 0xff

            if message["data"] == []:
                
                data = [address1] + [address2] + [0]
            else:
                data = [address1] + [address2] + message["data"]

            format_string = format_string = f"1s1B3s{len(data)}B"

            data_bytes = struct.pack(format_string, START, len(data), type, *data)
        
        elif message["type"] == "TST":

            START = "X".encode()
            type = "TST".encode()
            
            time_byte = struct.pack("d", message["data"])
            data_bytes = struct.pack("1s1B3s", START, len(time_byte), type)
            data_bytes = data_bytes + time_byte

        
        else: # LID, SON, IMU
            pass

        try:
            self.socket.sendall(data_bytes)
        except socket.error:
            self.socket.close()
            print(f"Disconnected from {self.HOST}")

    # receive
    def run(self):
        try:
            data_receive = self.socket.recv(5) # get 2 bytes first, X start of frame, 1 integer length of frame

            if data_receive:
                data = struct.unpack(f"1s1B3s", data_receive)
                if data[0].decode() == "X":
                    frame_length = data[1]
                    type = data[2].decode()
                else:
                    frame_length = 0
            else:
                frame_length = 0
            
            data_frame = self.socket.recv(frame_length)

            if data_frame:

                if type == "CAN":
                    data = struct.unpack(f"{frame_length}B", data_frame)
                    address, data = data[0], data[1:]
                    pub.sendMessage("can.send", message = {"address": address, "data": data})

                elif type == "TST":
                    data = struct.unpack("d", data_frame)
                    time_rec = data[0]
                    pub.sendMessage("ethernet.send", message = {"type": "TST", "data": time_rec})
                
                else: # LID, SON, IMU
                    pass

        except socket.error:
            self.socket.close()
            print(f"Disconnected from {self.HOST}")
        
if __name__ == "__main__":
    from CANHandler import CANHandler
    #from USBCameraClient import *
    EthernetClient = EthernetClient()
    CANHandler = CANHandler(250000)

    EthernetClient.start(30)
    CANHandler.start(30)
    
    from IMUReaderPi import *
    write() # IMU
    # USBCameraClient() # USB Camera



