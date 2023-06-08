import socket
import subprocess

# create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 8000))

print("Server is waiting for a client on port 8000")

# Define command line for video player
cmdline = ['vlc', '--demux', 'h264', '-']
player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)

try:
    while True:
        data, addr = server_socket.recvfrom(4096)
        print(f"received message from {addr}")

        if not data:
            break
        player.stdin.write(data)
finally:
    server_socket.close()
    player.terminate()

# DOES NOT WORK
