import socket
import socket, sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((HOST, PORT))

client_socket.send('Hello, server!'.encode('utf-8'))
data = client_socket.recv(1024)
print(f'Received from server: {data.decode("utf-8")}')

client_socket.close()