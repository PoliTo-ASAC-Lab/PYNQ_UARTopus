import selectors
import socket
import sys
from time import sleep
import queue
import threading
import types
import argparse
from typing import List

from pynq import MMIO
from pynq import Overlay
from datetime import datetime
sys.path.insert(1, './src')
from uartlite import *

DEBUG = False

def th_serial_dispatcher(UART_AXI_address, q_tx: queue.Queue, q_rx_l: List[queue.Queue], q_cmd: queue.Queue):
    wait_time = 0.0
    delta_t = 0.000001
    max_wait = 0.00001
    print(f"S: Connecting to the AXI UART adapter {hex(UART_AXI_address)}")
    uart = UartAXI(UART_AXI_address)
    print(f"S: Connected. Bridge started!")

    while True:
        try:
            q_cmd.get_nowait()
            break
        except queue.Empty:
            pass

        try:
            if uart.currentStatus()['RX_VALID'] & 1: # "if something arrives" (see ./src/uartlite.py)
                data = (uart.readLine()).encode()

                if DEBUG: print(f"S: Received {len(data)} bytes from {hex(UART_AXI_address)}. Sending to {len(q_rx_l)} clients")
                for q_rx in q_rx_l:
                    q_rx.put(data, block=True)

                if DEBUG: print(f"T: {data}")
                wait_time = 0.0
            else:
                wait_time = (wait_time + delta_t) if wait_time < max_wait else wait_time
                if wait_time > 0:
                    sleep(wait_time)
        except Exception as e:
            print(f"S: Bridge {hex(UART_AXI_address)} exception occurred in rx mode: {e}")

    print("S: Closing the bridge...!")


HOST = "127.0.0.1" # PYNQ
PORT = 6543
DFBR = 19200

# Arguments parsing
parser = argparse.ArgumentParser(description="Serial - TCP/IP Manhattan Bridge")
parser.add_argument('bridge_id', type=str, nargs='?', help="str: bridge arbitrary identifier.", default="###")
parser.add_argument('UART_AXI_address', type=str, nargs=1, help="hex: AXI_UART adapter address.")
parser.add_argument('tcp_port', type=int, nargs='?', help=f"int: TCP port to bridge. Default is {PORT}.", default=PORT)

args = parser.parse_args()

bridge_id = args.bridge_id
UART_AXI_address = int(args.UART_AXI_address[0],16)   
pport = args.tcp_port
sel = selectors.DefaultSelector()
q_tx = queue.Queue()
q_rx_l: List[queue.Queue] = []
q_cmd = queue.Queue()

# Overlay handle retrieval 
bit_path = "./src/UART_HW_2.bit"
print(f"[INFO] Getting HW overlay handle for {bit_path}...", end="", flush=True)
ol = Overlay(bit_path, download=False)
if not ol.is_loaded():
    exit("\n[ERROR] Bitstream not loaded, run overlay_init.py first!")
print("DONE!")

# Spawning the serial-UART dispatcher thread
th0 = threading.Thread(target=th_serial_dispatcher, args=(UART_AXI_address, q_tx, q_rx_l, q_cmd))

wait_time = 0.0
delta_t = 0.000001
max_wait = 0.00001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # https://stackoverflow.com/a/4466035
    s.bind((HOST, pport))
    s.listen()
    s.setblocking(False)
    sel.register(s, selectors.EVENT_READ, data=None)

    print(f"S: Waiting incoming connections on tcp://{HOST}:{pport}")
    th0.start()

    try:
        while True:
            evts = sel.select(timeout=1)
            for key, mask in evts:
                if key.data is None:
                    conn, addr = key.fileobj.accept()
                    print(f"S: New incoming connection from {addr}")
                    conn.setblocking(False)
                    qrx = queue.Queue()
                    q_rx_l.append(qrx)
                    data = types.SimpleNamespace(addr=addr, q_rx=qrx, q_rx_pos=len(q_rx_l) - 1)
                    events = selectors.EVENT_READ | selectors.EVENT_WRITE
                    sel.register(conn, events, data=data)

                else:
                    sock = key.fileobj
                    data = key.data
                    q_rx: queue.Queue = data.q_rx

                    if mask & selectors.EVENT_READ:
                        try:
                            recv_data = sock.recv(1024)
                        except ConnectionResetError:
                            recv_data = None

                        if recv_data:
                            print(f"S: New data from {data.addr}, {len(recv_data)} bytes")
                            print(f"C: {recv_data}")
                            q_tx.put(recv_data)
                        else:
                            print(f"S: Closing connection with {data.addr}")
                            q_rx_l.pop(data.q_rx_pos)
                            sel.unregister(sock)
                            sock.close()

                        wait_time = 0
                    else:
                        wait_time = (wait_time + delta_t) if wait_time < max_wait else wait_time
                        if wait_time > 0:
                            sleep(wait_time)

                    if mask & selectors.EVENT_WRITE:
                        if not q_rx.empty():
                            dt = q_rx.get(block=True)
                            sock.sendall(dt)
                            wait_time = 0.0
                        else:
                            wait_time = (wait_time + delta_t) if wait_time < max_wait else wait_time
                            if wait_time > 0:
                                sleep(wait_time)

    except KeyboardInterrupt:
        print("S: Interrupting...")
    finally:
        sel.close()

print(f"S: Trying to close the bridge...")
q_cmd.put(0)
th0.join()
