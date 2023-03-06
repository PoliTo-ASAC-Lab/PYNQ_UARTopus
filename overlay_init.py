from pynq import Overlay
bit_path = "./src/UART_HW_3.bit"
print(f"[INFO] Loading bitstream {bit_path}...", end="", flush=True)
ol_base = Overlay("base.bit", download=True)
ol = Overlay(bit_path, download=True)
print("DONE!")