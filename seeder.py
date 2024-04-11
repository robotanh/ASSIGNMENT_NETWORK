import subprocess
import re
import json
import socket
import os

class Seeder:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peer_port = 12346  # Use a different port for peer-to-peer communication
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
        self.socket.close()

    """

    SEND LIST OF FILE HAVING IN COMPUTER TO SEVER

    """
    def serve_file_piece(self):
        # Setup server to send file piece to other client
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', self.peer_port))
            s.listen()
            print("Serving file pieces on port:", self.peer_port)
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Assume data is the filename to send
                    filename = data.decode('ascii')
                    file_path = os.path.join('file_split', filename)
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            piece = f.read()
                            conn.sendall(piece)
                    else:
                        conn.sendall(b'File not found')
                print("Finished serving file piece.")

    def get_filenames_in_folder(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, 'file_split')
        filenames = os.listdir(folder_path)
        filenames = [f for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
        return filenames
    
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

        if 'Others client want to download piece' in received_message:
            self.close()  # Close connection with server
            self.serve_file_piece()  # Serve file piece to other client
            # Optionally, reconnect to main server after serving
            # self.connect()

    """

    SEND FLAG, IPADDRESS, PORT TO SEVER

    """
    def send_message(self):
        try:
            hostname = socket.gethostname()
            ipv4_address = socket.gethostbyname(hostname)
            message = {
                "flag": "SEEDER",
                "ip_address": ipv4_address,
                "port": 23456
            }
            self.socket.send(json.dumps(message).encode('utf-8'))
            received_message = self.receive_message()
            print('Received from the server:', received_message)
        except socket.gaierror:
            print("There was an error resolving the hostname.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def seeder_mode():
    host = '10.128.142.39'
    port = 12345
    client = Seeder(host, port)
    client.connect()
    client.send_message()
    client.close()
