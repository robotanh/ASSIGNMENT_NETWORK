import socket
import os
import json
import tqdm
from client_action import *

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host=None, port=None):
        if host is None and port is None:
            host, port = self.host, self.port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_message(self, message):
        self.socket.send(message.encode('ascii'))

    def receive_message(self):
        return self.socket.recv(1024).decode('ascii')

    def close(self):
        print(f"Closed connection with {self.host}:{self.port}")
        self.socket.close()

    """
    SEND LIST OF FILES THAT DIFFERENT FROM TORRENT FILE
    """

    def send_json_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'torrents', 'ALICE.json')  # Adjust file path
        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return

        with open(file_path, 'r') as f:
            """
            missing_pieces_json has the type
                "file_parts": [pieces]
            """
            missing_pieces_json =send_missing_pieces()
            if missing_pieces_json:
                self.send_message(missing_pieces_json)
                # received_message = self.receive_message()   
                self.received_message_from_seeder()


    def send_filenames_to_server(self):
        filenames = self.get_filenames_in_folder()
        if not filenames:
            print("No files found in the folder.")
            return

        filenames_str = '\n'.join(filenames)
        print("Sent list of filenames to server.")
        print(filenames_str)
        self.send_message(filenames_str)
        received_message = self.receive_message()
        print('Received from the server:', received_message)

    def get_filenames_in_folder(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, 'file_split')
        filenames = os.listdir(folder_path)
        filenames = [f for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
        return filenames
    

    def send_message_to_sever(self):
        try:
            hostname = socket.gethostname()
            ipv4_address = socket.gethostbyname(hostname)
            message = {
                "flag": "CLIENT",
                "ip_address": ipv4_address,
                "port": 23456
            }
            self.socket.send(json.dumps(message).encode('utf-8'))
            received_message = self.receive_message()          
            return received_message
        except socket.gaierror:
            print("There was an error resolving the hostname.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None
    """
    Recieve massage from seeder (which is a file) and save it in directory
    """
    def received_message_from_seeder(self):
        try:
            while True:
                file_name = self.socket.recv(1024).decode().strip()
                if not file_name:
                    print("No more files to receive or file name is empty.")
                    break  # No more files to receive

                file_size = ""
                while True:
                    char = self.socket.recv(1).decode()
                    if char == '\n':
                        break
                    file_size += char
                
                if file_size.strip() == "":
                    print("File size not received properly or is empty.")
                    continue  # Skip to the next file or end the loop
                
                file_size = int(file_size.strip())  # Ensure conversion to integer

                with open(file_name, "wb") as file:
                    progress = tqdm.tqdm(total=file_size, unit="B", unit_scale=True, desc=f"Receiving {file_name}")
                    received_size = 0
                    while received_size < file_size:
                        data = self.socket.recv(min(1024, file_size - received_size))
                        if not data:
                            print(f"Connection ended unexpectedly while receiving {file_name}.")
                            break
                        file.write(data)
                        received_size += len(data)
                        progress.update(len(data))
                    progress.close()
                    print(f"{file_name} received successfully.")
                file.close()
        except Exception as e:
            print(f"An error occurred while receiving file parts: {e}")
        finally:
            self.socket.close()




    
"""
when server return a list of peer, connect_with_peers get a list of peers and connect 
one by one to get pieces
"""
def connect_with_peers(peers_list_json):
    connected_peers = []

    # Convert JSON string back to a Python list of dictionaries
    peers_dict = json.loads(peers_list_json)
    peers_list = peers_dict.get("Peers", [])

    ip_address = None
    port = None
    for peer_info in peers_list:

        try:
            # peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ip_address = peer_info["ip_address"]
            port = peer_info["port"]

            client = Client(ip_address, port)
            client.connect()
            client.send_json_file() #send mising file to sever
            client.close()

            connected_peers.append(client)
            print(f"Connected to peer: {ip_address}:{port}")

        except ConnectionRefusedError:
            print(f"Connection to peer {ip_address}:{port} refused")
            client.close()
        except Exception as e:
            print(f"Error connecting to peer {ip_address}:{port}: {e}")
            print("Peer info:", peer_info)
            client.close()

    
def action(client):
    received_message = client.send_message_to_sever()
    # print('Received from the server:', received_message)
    connect_with_peers(received_message)

    
def client_mode():
    host = '192.168.1.3'
    port = 12345
    client = Client(host, port)
    client.connect()
    # client.send_json_file()
    # send_missing_pieces()
    action(client)
    client.close()
