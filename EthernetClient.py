# echo-client.py
import time
import socket
import struct
from pubsub import pub
from ModuleBase import Module

class EthernetClient(Module):
    def __init__(self):
        super.__init__()

        HOST = "169.254.196.165"  # The server's hostname or IP address
        PORT = 50000  # The port used by the server

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))

        pub.subscribe(self.message_listener, "ethernet.send")
    
    def message_listener(self, message):
        try:
            self.socket.sendall(message["data"])
        except socket.error:
            print("socket error")
            # TODO: deal with socket error

    
    def run(self):
        try:
            data_receive = self.socket.recv(1024)

            if data_receive:
                data = struct.unpack("{}B".format(len(data_receive)), data_receive)
                address, data = data[0], data[1:]

                pub.sendMessage("can.send", message = {"address": address, "data": [data]})

        except socket.error:
            print("socket error")
        
if __name__ == "__main__":
    from CANHandler import CANHandler
    EthernetClient = EthernetClient()
    CANHandler = CANHandler(250000)

    EthernetClient.start(30)
    CANHandler.start(30)

