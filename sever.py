import socket
import threading
import sys

def threaded(c, addr):
    with c:
        print(f"Connected to: {addr}")
        while True:
            data = c.recv(1024)
            if not data:
                print(f"Bye {addr}")
                break
            c.send(data)
        print(f"Connection closed with {addr}")

def main():
    host = '0.0.0.0'
    port = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f"Socket is bound to port {port}, and is listening...")

        try:
            while True:
                c, addr = s.accept()
                threading.Thread(target=threaded, args=(c, addr)).start()
        except KeyboardInterrupt:
            print("\nServer is shutting down.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            s.close()
            print("Socket closed.")

if __name__ == '__main__':
    main()
