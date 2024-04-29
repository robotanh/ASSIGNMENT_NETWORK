
...
# A torrent-like file sharing app
A centralized server keeps track of which clients are connected and what pieces of files stored on that client. 

Through tracker protocol, a client informs the server as to what files are contained in its local repository but does not actually transmit file data to the server.

The app is built with Python 3.10. To install the packages, run:
```bash
pip install -r requirements . txt
```
Next run the server: 
```bash
python server.py
```
To utilize the Torrent system, first, navigate to the project directory in your terminal. Then, to
start the server, run the following command:
```bash
python main.py
```
Then follow the instruction to select the necessary mode.
