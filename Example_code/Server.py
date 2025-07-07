import socket

# Set the IP address and port for the server
ip = '192.168.12.4'
port = 8002

# Create a TCP/IP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen()

print(f"Server IP: {ip}")
print(f"Server is listening on port {port}")

# Accept incoming connections
while True:
  client_socket, addr = server.accept()

  print(f"Connection from {addr} has been established.")

  # Receive the txt data from the client and write to file
  file = open('test_recieve.txt', 'wb')
  image_data = client_socket.recv(2048)

  # Continue receiving data until no more is sent
  while image_data:
    file.write(image_data)
    image_data = client_socket.recv(2048)

  file.close()