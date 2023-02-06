from pynq import Overlay
bit_path = "./src/UART_HW_2.bit"
print(f"[INFO] Loading bitstream {bit_path}...", end="", flush=True)
ol = Overlay(bit_path, download=False)
if not ol.is_loaded():
	ol.download()
	print("DONE!")
else:
	print("already loaded!")