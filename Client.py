import socket, sys, time

def run_test(host, port, measurement_type, num_probes, msg_size, server_delay):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))

    # Connection Setup Phase

    setup_message = f's {measurement_type} {num_probes} {msg_size} {server_delay}\n'

    client_socket.send(setup_message.encode('utf-8'))
    setup_response = client_socket.recv(1024).decode("utf-8")
    print(f'Received from server: {setup_response}')

    # Checking for a 200 response
    if setup_response[0:3] != "200":
        client_socket.close()
        exit()

    # Measurement Phase
    payload = '?' * msg_size
    rtt_vals = []
    tput_vals = []
    for probe_sequence_number in range(1, num_probes + 1):
        probe_message = f"m {probe_sequence_number} {payload}"
        begin_time = time.perf_counter_ns()
        client_socket.send(probe_message.encode("utf-8"))
        probe_response = client_socket.recv(msg_size + 128).decode("utf-8")
        end_time = time.perf_counter_ns()
        rtt = end_time - begin_time
        if measurement_type == "rtt":
            rtt_vals.append(rtt)
            print(f"Current RTT: {rtt/1000000} ms.")
        else:
            tput = 2 * len(probe_message) / rtt
            tput_vals.append(tput)
            print(f"Current TPUT: {tput * 8000000} kbps")
        
    if measurement_type == 'rtt':
        average = (sum(rtt_vals)/len(rtt_vals))/1000000
        print(f"The average {measurement_type} value is {(sum(rtt_vals)/len(rtt_vals))/1000000} ms.")
    else:
        average = (sum(tput_vals)/len(tput_vals))*8000000
        print(f"The average {measurement_type} value is {(sum(tput_vals)/len(tput_vals))*8000000} kbps")

    # Termination Phase
    client_socket.send("t\n".encode("utf-8"))
    termination_response = client_socket.recv(1024).decode("utf-8")
    print(f"Received from server: {termination_response}")
    print("Terminating connection...")
    client_socket.close()
    return average
    


if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    run_test(host, port, 'rtt', 10, 10, 0)