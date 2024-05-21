import serial
import time

# Configuration for the sender port
COM_PORT_SENDER = 'COM1'  # The paired port, adjust according to your setup
BAUD_RATE = 19200  # Should match the receiver's baud rate

try:
    with serial.Serial(COM_PORT_SENDER, BAUD_RATE, timeout=1) as ser_sender:
        print(f"Sending data to {COM_PORT_SENDER}...")
        ser_sender.write(b'27 H55T20L305\n')  # Sending test data
        time.sleep(1)  # Wait a bit for data to be sent
        print("Data sent.")
except Exception as e:
    print(f"Error: {e}")
