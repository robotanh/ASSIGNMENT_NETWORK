import socketserver
import json
import threading

# Global list of peers and a lock for thread-safe operations on this list
peers_list = []
lock = threading.Lock()

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        try:
            # Receive data from the client and decode it
            self.data = self.request.recv(1024).strip().decode('utf-8')
            self.data = json.loads(self.data)  # Parse the JSON data

            print(f"Connection from: {self.client_address[0]}")
            print(self.data)

            # Extract data from the received JSON
            ip_address = self.data.get("ip_address")
            port = self.data.get("port")
            flag = self.data.get("flag")

            # Initialize response_data dictionary
            response_data = {}

            # Process based on the flag
            with lock:
                if flag == "CLIENT":
                    # For CLIENT, send back the list of peers
                    response_data["Peers"] = peers_list
                elif flag == "SEEDER":
                    # For SEEDER, add the peer to the list if not already present
                    if all(peer["ip_address"] != ip_address or peer["port"] != port for peer in peers_list):
                        peers_list.append(self.data)
                        response_data["Peers"] = peers_list
                    else:
                        response_data["Peers"] = peers_list
                elif flag == "SEEDER_LOGOUT":
                    # For SEEDER_LOGOUT, remove the peer from the list
                    for peer in peers_list:           
                        if (peer["ip_address"] == ip_address and peer["port"] == port):
                            peers_list.remove(peer)
                    response_data["Peers"] = peers_list
                else:
                    response_data["failure_reason"] = "Invalid flag"

                # Log current state of peers list
                print("Currently connected clients:")
                for peer in peers_list:
                    print(peer)
                print("----------")
        except json.JSONDecodeError:
            response_data = {"error": "Invalid JSON format"}
        except Exception as e:
            response_data = {"error": str(e)}

        # Send back the JSON response
        response = json.dumps(response_data)
        self.request.sendall(response.encode('utf-8'))
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "", 12345

    # Create the server, binding to localhost on the specified port
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        print(f"Server listening on {HOST}:{PORT}")
        server.serve_forever()
