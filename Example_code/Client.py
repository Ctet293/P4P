import socket

# Set the IP address and port for the client
ip = '192.168.12.4'
port = 8002

# Create a TCP/IP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

# Open file to send
file = open('test_send.txt', 'rb')

# Read the file in chunks and send it to the server
image_data = file.read(2048)

# Continue sending data until the end of the file
while image_data:
  client.send(image_data)
  image_data = file.read(2048)

# Close the file and the socket
file.close()
client.close()