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

class USBEthernetClientHandler(Module):
    def __init__(self):
        super().__init__()

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.socket.bind(("", PORT))
        self.socket.listen()
    

class USBCameraServer(Module):

    # receive frames
    def run(self):
        # Receive the frame size from the client
        frame_size_data = client_socket.recv(struct.calcsize('<L'))
        if frame_size_data:
            frame_size = struct.unpack('<L', frame_size_data)[0]

            # Receive the frame data from the client
            frame_data = b''
            while len(frame_data) < frame_size:
                data = client_socket.recv(frame_size - len(frame_data))
                if not data:
                    break
                frame_data += data

            # Decode the MJPEG data and convert it to a BGR image
            frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

            cv2.imshow('Frame', frame)

            k = cv2.waitKey(1)
            if k == 27:
                self.stop()

