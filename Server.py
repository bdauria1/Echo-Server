import socket, sys, time

MEASUREMENT_TYPE = ''
NUM_PROBES = 0
MESSAGE_SIZE = 0
SERVER_DELAY = -1
PROBE_SEQUENCE_NUMBER = 0

def parse_setup_message(msg: str):
    msg_info = msg.split(' ')
    if len(msg_info) != 5:
        raise ValueError("Incorrect setup message")
    phase = msg_info[0]
    measurement_type = msg_info[1]
    num_probes = int(msg_info[2])
    message_size = int(msg_info[3])
    server_delay = float(msg_info[4].strip())
    if phase != 's':
        raise ValueError(f"Invalid phase: {phase}")
    if measurement_type not in ['rtt', 'tput']:
        raise ValueError(f"Invalid mesurement type: {measurement_type}")
    if num_probes <= 0:
        raise ValueError(f"Invalid number of probes: {num_probes}")
    if message_size <= 0:
        raise ValueError(f"Invalid message size: {message_size}")
    if server_delay < 0:
        raise ValueError(f"Invalid server delay: {server_delay}")
    return measurement_type, num_probes, message_size, server_delay


def parse_probe_message(msg: str, current_probe):
    msg_info = msg.split(' ')
    if len(msg_info) != 3:
        raise ValueError("Incorrect setup message")
    phase = msg_info[0]
    probe_seq_num = int(msg_info[1])
    payload = msg_info[2].strip()

    if phase != 'm':
        raise ValueError(f"Incorrect phase: {phase}")
    if probe_seq_num != current_probe:
        raise ValueError(f"Incorrect probe sequence number: {probe_seq_num}")
    if len(payload) != MESSAGE_SIZE:
        raise ValueError(f"Incorrect payload size")
    
    return 


PORT = int(sys.argv[1])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '0.0.0.0'
server_socket.bind((host, PORT))

server_socket.listen(5)


print(f'Server started on {host}:{PORT}')
print('Waiting for a connection...')

while True:
    # Connection Setup Phase
    client_socket, addr = server_socket.accept()
    print(f'Connection established with: {addr}')

    setup_message = client_socket.recv(1024)
    try:
        MEASUREMENT_TYPE, NUM_PROBES, MESSAGE_SIZE, SERVER_DELAY = parse_setup_message(setup_message.decode('utf-8'))
        client_socket.sendall("200 OK: Ready".encode("utf-8"))
        print(f'Setup Message received from client: {setup_message.decode("utf-8")}')
    except Exception as e:
        print(f"Error: {e}")
        client_socket.sendall("404 ERROR: Invalid Connection Setup Message".encode("utf-8"))
        client_socket.close()
        continue


    # Measurement Phase
    for probe_sequence_num in range(1, NUM_PROBES+1):
        probe_message = bytes()
        while len(probe_message) < (MESSAGE_SIZE + 4 + len(str(probe_sequence_num))):
            data = client_socket.recv(1)
            probe_message += data

        try:
            parse_probe_message(probe_message.decode("utf-8"), probe_sequence_num)
            time.sleep(SERVER_DELAY)
            client_socket.sendall(probe_message)
            print(f'Probe Message received from client: {probe_message.decode("utf-8")}')
        except Exception as e:
            print(f"Error: {e}")
            client_socket.sendall("404 ERROR: Invalid Measurement Message".encode("utf-8"))
            client_socket.close()
            continue

    # Termination Phase
    term_message = client_socket.recv(2).decode("utf-8")
    if term_message == "t\n":
        client_socket.sendall("200 OK: Closing Connection".encode("utf-8"))
    else:
        client_socket.sendall("404 ERROR: Invalid Connection Termination Message".encode("utf-8"))

    client_socket.close()