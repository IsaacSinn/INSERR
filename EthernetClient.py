# echo-client.py
import time
import socket
import struct
from pubsub import pub
from ModuleBase import Module

class EthernetClient(Module):
    def __init__(self):
        super().__init__()

        self.HOST = "10.239.246.80"  # The server's hostname or IP address
        self.PORT = 50000  # The port used by the server

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.HOST, self.PORT))

        print(f"Connected to server {self.HOST}")

        pub.subscribe(self.message_listener, "ethernet.send")
    
    def message_listener(self, message):

        if message["type"] == "CAN":

            type = data[0].encode()
            data = [message["address"]] + message["data"]

            format_string = f"{len(type)}s{len(data)}B"

            data_bytes = struct.pack(format_string, *data)

        
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
            data_receive = self.socket.recv(1024)

            if data_receive:
                data = struct.unpack(f"3s{len(data_receive) - 3}B", data_receive)

                if data[0].decode() == "CAN": # CAN
                    address, data = data[1], data[2:]
                    pub.sendMessage("can.send", message = {"address": address, "data": data})
                else: # LID, SON, IMU
                    type, data = data[0].decode(), data[1:]
                    pub.sendMessage(f"{type}.send", message = {"data": data})

        except socket.error:
            self.socket.close()
            print(f"Disconnected from {self.HOST}")
        
if __name__ == "__main__":
    from CANHandler import CANHandler
    EthernetClient = EthernetClient()
    CANHandler = CANHandler(250000)

    EthernetClient.start(30)
    CANHandler.start(30)

