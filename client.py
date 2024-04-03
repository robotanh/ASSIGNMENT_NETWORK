import socket

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
    host = '192.168.100.17'
    port = 12345
    client = Client(host, port)
    client.connect()
    client.start_communication()
    client.close()
