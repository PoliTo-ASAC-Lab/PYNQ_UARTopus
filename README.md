# PYNQ_UARTopus
Python platform to use a TUL PYNQ-Z2 development board to virtualize up to 12 UART connections (tx+rx) over TCP-IP

### UART interfaces pinout
ID | AXI_BASE_ADDRESS | TX_pin | RX_pin
|  :-: |  :-: |  :-: | :-: |
UART_1 | 0x42C10000 | PMODA-1 | PMODA-7 
UART_2 | 0x42C20000 | PMODA-2 | PMODA-8
UART_3 | 0x42C30000 | PMODA-3 | PMODA-9
UART_4 | 0x42C40000 | PMODA-4 | PMODA-10
UART_5 | 0x42C50000 | PMODB-1 | PMODB-7 
UART_6 | 0x42C60000 | PMODB-2 | PMODB-8 
UART_7 | 0x42C70000 | PMODB-3 | PMODB-9 
UART_8 | 0x42C80000 | PMODB-4 | PMODB-10 
UART_9 | 0x42C90000 | AR-0 | AR-1
UART_10 | 0x42CA0000 | AR-2 | AR-3
UART_11 | 0x42CB0000 | AR-4 | AR-5
UART_12 | 0x42C00000 | AR-6 | AR-7

### UART interfaces pinout
![UART_interfaces_pinout](https://user-images.githubusercontent.com/37268662/217187596-a422d963-93b3-46a0-aad0-eeff5566b696.png)
