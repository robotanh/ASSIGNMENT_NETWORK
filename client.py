import socket
import os
import json
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
        self.socket.close()

    def send_json_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'torrents', 'ALICE.json')  # Adjust file path
        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return

        with open(file_path, 'r') as f:
            json_data = json.load(f)
            json_str = json.dumps(json_data)
            #print(json_str)
            self.send_message(json_str)
            received_message = self.receive_message()
            print('Received from the server:', received_message)


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

if __name__ == '__main__':
    host = '192.168.1.3'
    port = 12345
    client = Client(host, port)
    client.connect()
    client.send_json_file()
    send_missing_pieces()

    client.close()
