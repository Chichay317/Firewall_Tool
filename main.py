import socket
import time

allowed_ips = ["192.168.1.1", "192.168.1.2"]
blocked_ips = ["192.168.1.100"]
allowed_ports = [80, 443]
blocked_ports = [22]

connection_times = {}

MAX_REQUESTS_PER_MINUTE = 5

def is_ip_allowed(ip):
    if ip in allowed_ips:
        return True
    elif ip in blocked_ips:
        return False
    return True

def is_port_allowed(port):
    if port in allowed_ports:
        return True
    elif port in blocked_ports:
        return False
    return True

def is_rate_limited(ip):
    current_time = time.time()

    if ip not in connection_times:
        connection_times[ip] = []

    connection_times[ip] = [timestamp for timestamp in connection_times[ip] if current_time - timestamp < 60]

    if len(connection_times[ip]) >= MAX_REQUESTS_PER_MINUTE:
        return True

    connection_times[ip].append(current_time)
    return False

def start_firewall_server(host='0.0.0.0', port=8080):
    print(f"Starting server on {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(5)

        print("Server is listening for incoming connections...")

        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                client_ip = client_address[0]
                client_port = client_address[1]

                print(f"Connection attempt from {client_ip}:{client_port}")

                if not is_ip_allowed(client_ip):
                    print(f"Connection from {client_ip} blocked (IP not allowed).")
                    client_socket.close()
                    continue

                if is_rate_limited(client_ip):
                    print(f"Connection from {client_ip} blocked (Rate limit exceeded).")
                    client_socket.close()
                    continue

                if not is_port_allowed(client_port):
                    print(f"Connection from {client_ip}:{client_port} blocked (Port not allowed).")
                    client_socket.close()
                    continue

                print(f"Connection from {client_ip}:{client_port} allowed.")
                client_socket.sendall(b"Hello, your connection is allowed!")


if __name__ == "__main__":
    start_firewall_server()
