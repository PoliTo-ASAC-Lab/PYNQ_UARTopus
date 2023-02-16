import socket
import time

IP = "127.0.0.1"
TCP_PORT = int(input())

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_STREAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # https://stackoverflow.com/a/4466035
sock.connect((IP, TCP_PORT))

print(f"Listening to TCP://{IP}:{TCP_PORT}")

while True:
    time.sleep(1)
    print("sending")
    sock.sendall("ciao".encode())
    #try:
    #    recv_data = sock.recv(1024)
    #except ConnectionResetError:
    #    recv_data = None
#
    #if recv_data:
        #print(f"S: New data from device, {len(recv_data)} bytes")
    #    print(recv_data.decode(),end="")
