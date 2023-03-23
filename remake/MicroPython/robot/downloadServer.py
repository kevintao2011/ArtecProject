import socket

# Connect to the ESP32 board over a remote socket
ip = '192.168.1.83'  # Replace with the IP address of your ESP32 board
port = 1234  # Replace with a free port number on your ESP32 board
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))

# Open the Python script file and read the data
with open('main.py', 'rb') as f:
    script_data = f.read()

# Send the Python script data over the socket connection
sock.send(script_data)

# Close the socket connection
sock.close()
