PORT = int(sys.argv[1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
server_socket.bind((host, PORT))

server_socket.listen(5)

print(f'Server started on {host}:{PORT}')
print('Waiting for a connection...')

while True:
    client_socket, addr = server_socket.accept()
    print(f'Connection established with: {addr}')

    data = client_socket.recv(1024)
    if not data:
        print(f'Client {addr} disconnected')
        client_socket.close()
        continue
    
    print(f'Received from client: {data.decode("utf-8")}')
    client_socket.send(data)
    client_socket.close()