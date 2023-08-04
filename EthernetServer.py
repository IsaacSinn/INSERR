'''
Ethernet Handler Module

Subsribe Topics:
    can.send

Publish Topics:
    Ethernet.log
'''

from ModuleBase import Module
from ModuleBase import ModuleManager
from pubsub import pub
import socket
import struct
#######TO REMOVE
import time

class EthernetHandler(Module):
    def __init__(self):
        super().__init__()

        pub.subscribe(self.message_listener, "ethernet.send")
        self.conn = None
        self.addr = None
        self.connected = False
    
    def update_conn(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.connected = True
    
    def message_listener(self, message):
        
        # constructing data_byte struct
        # if message is CAN: START, length of data, "CAN", data
        if message["type"] == "CAN":

            START = "X".encode()
            type = "CAN".encode()

            data = [message["address"]] + message["data"]

            format_string = f"1s1B3s{len(data)}B"

            data_bytes = struct.pack(format_string, START, len(data), type, *data)
        
        elif message["type"] == "TST":

            START = "X".encode()
            type = "TST".encode()
            start_time = time.time()

            time_byte = struct.pack("d", start_time)

            data_bytes = struct.pack("1s1B3s", START, len(time_byte), type)

            data_bytes = data_bytes + time_byte
        
        # else type is LID, SON, IMU
        else:
            pass

        # send
        if self.connected:
            try:
                self.conn.sendall(data_bytes)
            except socket.error:
                print(f"Disconnect from {self.addr}")
                self.conn = None
                self.connected = False

    def run(self):

        # receive
        if self.connected:
            try:
                data_receive = self.conn.recv(5)

                if data_receive:
                    data = struct.unpack(f"1s1B3s", data_receive)
                    if data[0].decode() == "X":
                        frame_length = data[1]
                        type = data[2].decode()
                    else:
                        frame_length = 0
                else:
                    frame_length = 0
                
                data_frame = self.conn.recv(frame_length)

                if data_frame:
                    
                    if type == "CAN":
                        data = struct.unpack(f"{frame_length}B", data_frame)
                        address, data = data[0], data[1:]
                        pub.sendMessage("can.receive", message = {"address": address, "data": data})
                    
                    elif type == "TST":
                        data = struct.unpack("d", data_frame)
                        time_rec = data[0]
                        print((time.time() - time_rec))
                    
                    else: # LID, SON, IMU
                        pass

            except socket.error:
                print(f"Disconnect from {self.addr}")
                self.conn = None
                self.connected = False

# connects to a new client when available
class EthernetClientHandler(Module):
    def __init__(self):
        super().__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", 50001))
        self.socket.listen()
        self.EthernetHandler = EthernetHandler()
        mm = ModuleManager()
        mm.register((self.EthernetHandler, 30))
        mm.start("EthernetHandler")
    
    def run(self):
        self.conn, self.addr = self.socket.accept()
        print(f"Connected to {self.addr}")
        self.EthernetHandler.update_conn(self.conn, self.addr)


class TestEthernetHandler(Module):
    def __init__(self):
        super().__init__()

    def run(self):
        pub.sendMessage("ethernet.send", message = {"type": "TST", "address": 0x15, "data": [0x20, 0x10, 0x00]})

if __name__ == "__main__":
    EthernetClientHandler = EthernetClientHandler()
    TestEthernetHandler = TestEthernetHandler()

    EthernetClientHandler.start(1)
    TestEthernetHandler.start(1)
        



