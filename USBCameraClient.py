import cv2
import socket
import struct
import time

IP = '192.168.50.198'
PORT = 8080

def connect_to_server():
    # Create a socket and connect to the server
    client_socket = socket.socket()
    while True:
        try:
            client_socket.connect((IP, PORT))
            print('Connection established')
            time.sleep(1)
            break
        except ConnectionRefusedError:
            print('No connection established. Retrying in 3 seconds...')
            time.sleep(3)
    return client_socket

def camera(cam_num, cam_format, v_width, v_height, v_fps):
    # Start the camera
    cam = cv2.VideoCapture(cam_num, cv2.CAP_V4L2)

    # Set the video format
    cam.set(cv2.CAP_PROP_CONVERT_RGB, 0)
    fourcc = cv2.VideoWriter_fourcc(*cam_format)
    cam.set(cv2.CAP_PROP_FOURCC, fourcc)
    #cam.set(cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, v_width)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, v_height)
    cam.set(cv2.CAP_PROP_FPS, v_fps)

    return cam





def USBCameraClient():
    while True:
        # Read the frame
        ret, image = cam0.read()
        # Convert the frame to a byte array
        frame_data = image.tobytes()
        
        try:
            # Send the frame data through the socket
            client_socket.sendall(struct.pack('<L', len(frame_data)) + frame_data)
        except (BrokenPipeError, ConnectionResetError):
            print('Connection lost. Reconnecting...')
            client_socket.close()
            client_socket = connect_to_server()
        
        k = cv2.waitKey(1)
        if k == 27:
            break

    # Release everything if job is finished
    cam0.release()
    client_socket.close()
    cv2.destroyAllWindows()

# Connect to the server
client_socket = connect_to_server()

# Start camera
cam0 = camera(0, 'MJPG', 1920, 1080, 60)

USBCameraClient()