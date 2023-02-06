# PYNQ_UARTopus
Python platform to use a TUL PYNQ-Z2 development board to virtualize up to 12 UART connections over TCP-IP

## UART interfaces pinout
- UART_1 (AXI BASE ADDR. 0x42C10000)
tx_1 --> PMODA pin 1 
rx_1 --> PMODA pin 7 

- UART_2 (AXI BASE ADDR. 0x42C20000)
tx_2 --> PMODA pin 2 
rx_2 --> PMODA pin 8

- UART_3 (AXI BASE ADDR. 0x42C30000)
tx_3 --> PMODA pin 3 
rx_3 --> PMODA pin 9

- UART_4 (AXI BASE ADDR. 0x42C40000)
tx_4 --> PMODA pin 4 
rx_4 --> PMODA pin 10

- UART_5 (AXI BASE ADDR. 0x42C50000)
tx_5 --> PMODB pin 1  
rx_5 --> PMODB pin 7 

- UART_6 (AXI BASE ADDR. 0x42C60000)
tx_6 --> PMODB pin 2  
rx_6 --> PMODB pin 8 

- UART_7 (AXI BASE ADDR. 0x42C70000)
tx_7 --> PMODB pin 3  
rx_7 --> PMODB pin 9 

- UART_8 (AXI BASE ADDR. 0x42C80000)
tx_8 --> PMODB pin 4  
rx_8 --> PMODB pin 10 

- UART_9 (AXI BASE ADDR. 0x42C90000)
tx_9 --> Arduino AR0
rx_9 --> Arduino AR1

- UART_10 (AXI BASE ADDR. 0x42CA0000)
tx_10 --> Arduino AR2
rx_10 --> Arduino AR3

- UART_11 (AXI BASE ADDR. 0x42CB0000)
tx_11 --> Arduino AR4
rx_11 --> Arduino AR5

- UART_12 (AXI BASE ADDR. 0x42C00000)
tx_12 --> Arduino AR6
rx_12 --> Arduino AR7