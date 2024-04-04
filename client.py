import socket
import os

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_message(self, message):
        self.socket.send(message.encode('ascii'))

    def receive_message(self):
        return self.socket.recv(1024).decode('ascii')

    def close(self):
        self.socket.close()

    def get_filenames_in_folder(self):
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(current_dir, 'file')
        
        # List all files in the 'file' directory
        filenames = os.listdir(folder_path)
        # Filter out directories, keep file names
        filenames = [f for f in filenames if os.path.isfile(os.path.join(folder_path, f))]
        return filenames
    def send_filenames_to_server(self):
        filenames = self.get_filenames_in_folder()
        if not filenames:
            print("No files found in the folder.")
            return

        filenames_str = '\n'.join(filenames)
        while True:
            print("Sent list of filenames to server.")
            print(filenames_str)
            #send
            self.send_message(filenames_str)
            received_message = self.receive_message()
            print('Received from the server:', received_message)
            ans = input('\nDo you want to continue(y/n): ')
            if ans != 'y':
                break
    
    def start_communication(self):
        message = "shaurya says "
        while True:
            self.send_message(message)
            received_message = self.receive_message()
            print('Received from the server:', received_message)
            ans = input('\nDo you want to continue(y/n): ')
            if ans != 'y':
                break

if __name__ == '__main__':
    host = '192.168.1.3'
    port = 12345
    client = Client(host, port)
    client.connect()
    #connect to sever

    client.send_filenames_to_server()
    client.close()
