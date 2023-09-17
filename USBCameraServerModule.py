import socket
import struct
import threading
import queue
import numpy as np
import cv2 # pip install opencv-python
from ModuleBase import Module
from ModuleBase import ModuleManager
from pubsub import pub

PORT = 8080

class USBCameraHandler(Module):
    def __init__(self):
        super().__init__()

        self.conn = None
        self.addr = None
        self.connected = False

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.bind(("", PORT))
        self.socket.listen()
        self.wait_for_client()
    
    # waits for client connection
    def wait_for_client(self):
        while True:
            self.conn, self.addr = self.socket.accept()
            self.connected = True
            print(f"USB Connected {self.addr}")
            break
    
    # receives camera frame and publish it out
    def run(self):
        if self.connected:
            try:

                # Receive the frame size from the client
                frame_size_data = self.conn.recv(struct.calcsize('<L'))
                if frame_size_data:
                    frame_size = struct.unpack('<L', frame_size_data)[0]

                    # Receive the frame data from the client
                    frame_data = b''
                    while len(frame_data) < frame_size:
                        data = self.conn.recv(frame_size - len(frame_data))
                        if not data:
                            break
                        frame_data += data

                    # Decode the MJPEG data and convert it to a BGR image
                    frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                    pub.sendMesage("usb")
            
            except socket.error:
                print(f"USB Disconnected from {self.addr}")
                self.connected = False
                self.socket.close()
                self.wait_for_client()

