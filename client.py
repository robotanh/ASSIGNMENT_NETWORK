import socket
import os
import json
import tqdm
import sys
from torrent_action import *

class Client:
    def __init__(self, host, port,torrent_manager):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.torrent_manager = torrent_manager

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
        # has bug to fix
        missing_pieces_json = self.torrent_manager.send_missing_pieces()
        if missing_pieces_json:
            self.send_message(missing_pieces_json)
            # print("Sended:"+ missing_pieces_json)
            # received_message = self.receive_message()   
            self.received_message_from_seeder()



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
            file_name = None
            file_size = None
            file_data = b""
            progress = None
            file_path = "client_folder"
            buffer = ""

            while True:
                chunk = self.socket.recv(1024).decode('utf-8', errors='ignore')
                buffer += chunk
                while '\n' in buffer:
                    msg, buffer = buffer.split('\n', 1)  # Process each complete message one at a time
                    if ":" not in msg:
                        print(f"[CLIENT] Invalid message format: {msg}")
                        continue

                    cmd, data = msg.split(":", 1)

                    if cmd == "FILENAME":
                        file_name = data.strip()
                        print(f"[CLIENT] Received the filename: {file_name}.")

                    elif cmd == "FILESIZE":
                        file_size = int(data.strip())
                        print(f"[CLIENT] Received the size: {file_size} bytes.")
                        # if progress:  # Close any existing progress bar
                        #     progress.close()
                        # progress = tqdm.tqdm(total=290, unit="B", unit_scale=True, desc=f"Receiving {file_name}", ascii=True, colour='green')

                    elif cmd == "FILEDATA" and file_name and file_size:
                        print(f"[CLIENT] Receiving the file data.")
                        file_path = os.path.join(file_path, file_name)
                        data_bytes = data.encode('utf-8', errors='ignore')
                        progress = tqdm.tqdm(total=len(data_bytes), unit="B", unit_scale=True, desc=f"Receiving {file_name}", ascii=True, colour='green')
                        with open(file_path, "ab") as file:  # Use append mode
                            file.write(data_bytes)
                        if progress:
                            progress.update(len(data_bytes))  # Update progress with the length of bytes actually written

                    elif cmd == "FINISH":
                        if progress:
                            progress.close()
                        print(f"{file_name} received successfully. {data}")
                        file_name = None
                        file_size = None
                        file_data = b""
                        file_path = "client_folder"  # Reset the file path
                        progress = None

                    elif cmd == "CLOSE":
                        self.socket.close()
                        print(f"[CLIENT] {data}")
                        return
        except Exception as e:
            print(f"An error occurred while receiving file parts: {e}")
            sys.exit(1)



    
"""
when server return a list of peer, connect_with_peers get a list of peers and connect 
one by one to get pieces
"""
def connect_with_peers(peers_list_json, torrent_manager):

    try:
        # Convert JSON string back to a Python list of dictionaries
        peers_dict = json.loads(peers_list_json)
        peers_list = peers_dict.get("Peers", [])
    except json.JSONDecodeError:
        print("Failed to decode JSON from provided string")
    except Exception as e:
        print(f"An unexpected error occurred while decoding JSON: {e}")

    for peer_info in peers_list:
        ip_address = peer_info.get("ip_address")
        port = peer_info.get("port")
        if not ip_address or not port:
            print("Invalid IP address or port:", peer_info)
            continue

        client4peer = None
        try:
            client4peer = Client(ip_address, port, torrent_manager)
            client4peer.connect()
            client4peer.send_json_file()  # Send missing file to server
            print(f"Connected to peer: {ip_address}:{port}")

        except ConnectionRefusedError:
            print(f"Connection to peer {ip_address}:{port} refused")

        except socket.timeout:
            print(f"Timeout occurred when connecting to {ip_address}:{port}")

        except socket.error as sock_err:
            print(f"Socket error when connecting to {ip_address}:{port}: {sock_err}")

        except Exception as e:
            print(f"Error connecting to peer {ip_address}:{port}: {e}")
            print("Peer info:", peer_info)

        finally:
            if client4peer is not None:
                try:
                    client4peer.close()
                except Exception as e:
                    print(f"Error closing connection to {ip_address}:{port}: {e}")

   
    
def action(client,torrent_manager):
    received_message = client.send_message_to_sever()
    # print('Received from the server:', received_message)
    connect_with_peers(received_message,torrent_manager)

    
def client_mode(host,port,torrent_manager):
    client = Client(host, port,torrent_manager)
    client.connect()
    # client.send_json_file()
    # send_missing_pieces()
    action(client,torrent_manager)
    client.close()
