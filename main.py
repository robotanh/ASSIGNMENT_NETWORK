
from client import *
from seeder import *
from torrent_action import *


mode = input("Enter 1 or 2: ")

if mode == "1":
    torrent_manager = TorrentManager()
    host , port = torrent_manager.get_server_info()
    client_mode(host,port,torrent_manager)
elif mode == "2":
    torrent_manager = TorrentManager()
    host , port = torrent_manager.get_server_info()
    seeder_mode(host,port)
else:
    print("Invalid input. Please enter 1 or 2.")