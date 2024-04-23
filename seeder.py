import subprocess
import re
import json
import socket
import os
import sys


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
        print(f"Closed connection with {self.host}:{self.port}")
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
    def send_message_to_sever(self):
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

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)  # Maximum number of queued connections
            print(f"Server listening on {self.host}:{self.port}...")
            self.handle_connections()
        except KeyboardInterrupt:
            self.shutdown()
    def send_file_parts(self,client_socket, file_paths):
        try:
            for part in file_paths:
                file_path = os.path.join("file_split", part)
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)

                # Send file name
                client_socket.send(f"FILENAME:{file_name}\n".encode())
                print(f"[SEEDER] Sent filename: {file_name}")

                # Send file size
                client_socket.send(f"FILESIZE:{file_size}\n".encode())
                print(f"[SEEDER] Sent filesize: {file_size} bytes")

                # Send file data
                with open(file_path, "rb") as file:
                    chunk = file.read(1024)
                    while chunk:
                        client_socket.send(f"FILEDATA:{chunk}\n".encode())  # Assuming binary file and UTF-8 encoding issues
                        chunk = file.read(1024)

                # Send finish message
                client_socket.send("FINISH:File transfer complete.\n".encode())
                print(f"[SEEDER] File transfer complete for {file_name}")
            
            client_socket.send("CLOSE:Sended all files need\n".encode())    
            print(f"[SEEDER] End with {file_name}")
        except Exception as e:
            print(f"[SEEDER] An error occurred: {e}")
        finally:
            # Assuming that the socket should not be closed here to allow multiple files to be sent
            print(f"[SEEDER] Done sending {file_name}")



    def handle_client_connection(self, client_socket):
        try:
            # Receive the request from the client
            request_data = client_socket.recv(1024).decode('utf-8')
            request_parts = json.loads(request_data)["file_parts"]
            
            # Send the requested file parts to the client
            self.send_file_parts(client_socket, request_parts)
        except Exception as e:
            print(f"Error occurred: {e}")

    def handle_connections(self):
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Connection from {client_address} has been established.")
                self.handle_client_connection(client_socket)
            except Exception as e:
                print(f"Error accepting connections: {e}")


    def handle_client(self, client_socket):
        try:
            while True:
                data = client_socket.recv(1024)  # Buffer size
                if not data:
                    break
                print(f"Received from client: {data.decode()}")
                client_socket.sendall(data)
        except ConnectionResetError:
            pass  # Client closed the connection abruptly
        finally:
            client_socket.close()
            print(f"Closed connection with {client_socket}")

    def shutdown(self):
        print("\nKeyboard interrupt detected. Shutting down the server...")
        self.server_socket.close()
        sys.exit(0)

def action():
    HOST = '0.0.0.0'
    PORT = 23456
    server = Server(HOST, PORT)
    server.start()


def seeder_mode(host,port):
    client = Seeder(host, port)
    client.connect()
    client.send_message_to_sever()
    action()
    client.close()
