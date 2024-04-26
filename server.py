import socket
import threading
import sys
import json
import socketserver

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


# List of currently connected clients 
peers_list = []
lock = threading.Lock()


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    # def handle(self):
    #     # self.rfile is a file-like object created by the handler;
    #     # we can now use e.g. readline() instead of raw recv() calls
    #     self.data = self.request.recv(1024).strip()
    #     print("{} wrote:".format(self.client_address[0]))
    #     print(self.data)
    #     # Likewise, self.wfile is a file-like object used to write back
    #     # to the client
    #     self.request.sendall(self.data.upper())

    def handle(self): 
        # self.request is the TCP socket connected to the client 
        self.data = self.request.recv(1024).decode('utf-8')
        self.data = json.loads(self.data)
        print(f"Connection from: {self.client_address[0]}")
        ip_address = self.data.get("ip_address")
        port = self.data.get("port")
        flag = self.data.get("flag")

        with lock: 
            response_data = {
                "Peers": peers_list
            }

            if (flag != "CLIENT"): 
                response_data.clear()
                response_data["failure_reason"] = "Not client"
            else: 
                if all(self.data["ip_address"] != peer["ip_address"] and self.data["port"] != peer["port"] for peer in peers_list):
                    peers_list.append(self.data)

                print("Currently connected clients:")
                for peer in peers_list:
                    print(peer)
                print("----------")          
        response = json.dumps(response_data)
        self.request.sendall(response.encode('utf-8'))  

if __name__ == "__main__":
    HOST, PORT = "", 12345

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print(f"Server listening on host:{HOST}, port:{PORT}")
        server.serve_forever()
