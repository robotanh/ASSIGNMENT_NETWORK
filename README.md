
...
# A torrent-like file sharing app
A centralized server keeps track of which clients are connected and what pieces of files stored on that client. 

Through tracker protocol, a client informs the server as to what files are contained in its local repository but does not actually transmit file data to the server.
=======
client.py:
    - include client_action.py
    - xử lý file torrent (json) trong đó, so sánh các file trong folder tương ứng với nội dung trong torrent. Liệt kê ra những file trong folder không có và gửi cho server

seeder (client online để gửi piece): 
	Server gửi về (string type):
	- "INFO": thì seeder sẽ gửi list file (string type) bao gồm tên các piece
	- "SEND": thì seeder sẽ ngắt kết nối với sever và tự setup thành 1 sever với thằng cần download piece và gửi piece

