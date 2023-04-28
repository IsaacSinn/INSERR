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
        data = [message["address"]] + message["data"]
        data_bytes = struct.pack("{}B".format(len(data)), *data)

        # send
        if self.connected:
            try:
                self.conn.sendall(data_bytes)
                print(f"send: {data_bytes}")
            except socket.error:
                print(f"Disconnect from {self.addr}")
                self.conn = None
                self.connected = False

    def run(self):

        # receive
        if self.connected:
            try:
                data_receive = self.conn.recv(1024)
                if data_receive:
                    print(f"receive: {data_receive}")
            except socket.error:
                print(f"Disconnect from {self.addr}")
                self.conn = None
                self.connected = False
    
    # need to re-run rpi program when ethernet disconnect

# connects to a new client when available
class EthernetClientHandler(Module):
    def __init__(self):
        super().__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", 50000))
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
        pub.sendMessage("ethernet.send", message = {"address": 0xFF, "data": [0xAA]})

if __name__ == "__main__":
    EthernetClientHandler = EthernetClientHandler()
    TestEthernetHandler = TestEthernetHandler()

    EthernetClientHandler.start(1)
    TestEthernetHandler.start(1)
        



