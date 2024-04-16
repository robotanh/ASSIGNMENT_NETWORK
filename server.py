import socket
import threading
import sys
import threading
import time  

"""
Format of c: 
<
 socket.socket fd=504, 
 family=AddressFamily.AF_INET,  # IPv4
 type=SocketKind.SOCK_STREAM,   # stream-oriented => TCP
 proto=0,                       # unspecified since it is TCP
 laddr=('172.31.176.1', 12345), # local address
 raddr=('172.31.176.1', 55863)  # remote address
>

# JSON data to be stored
data = {
    "name_file": "ALICE.txt",
    "ip_address": "192.168.1.3",
    "pieces": files
}

{
    "flag": "SEEDER",
    "ip_address": "192.168.1.3"
    "port": "23456"
}

• peer id: peer's self-selected ID, as described above for the tracker request (string)
• ip: peer's IP address either IPv6 (hexed) or IPv4 (dotted quad) or DNS name (string)
• port: peer's port number (integer)

"""
import socket
import json

peers_list = []
lock = threading.Lock()

def handle_peer_connection(client_socket,client_address):
    request = client_socket.recv(1024).decode('utf-8')
    try:
        request_data = json.loads(request)

        ip_address = request_data.get("ip_address")
        port = request_data.get("port")
        flag = request_data.get("flag")

        with lock: 
            response_data = {
            "Peers": peers_list
            }
            if (flag != "CLIENT"):
                peers_list.append({
                    "flag": flag,
                    "ip_address": ip_address,
                    "port": port,
                })
                response_data.clear()
                response_data['failure_reason'] = "Not client"
            else:
                print("Currently connected clients:")
                for peer in peers_list:
                    print(peer)
               
        # Here, you could perform any processing with the received data
        # Write the data to a buffer to store
        # Send back the IP address to the client
        # Add client information to the list of connected clients
        # Print the list of connected clients
        
        response = json.dumps(response_data)
        client_socket.send(response.encode('utf-8'))
        print(f"Closed connection with {client_address[0]}:{client_address[1]}")
    except json.JSONDecodeError:
        print("Invalid JSON received")
    except KeyboardInterrupt: 
        print("leuleu")
    client_socket.close()

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5) # Max of 5 peers 
    print(f"Server listening on host:{host}, port:{port}")

    while True:
        client_socket, client_address = server_socket.accept()

        print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        handle_peer_connection(client_socket,client_address)


if __name__ == '__main__':
    start_server('', 12345)
