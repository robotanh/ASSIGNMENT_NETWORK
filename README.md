
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
To utilize the Torrent system, first, navigate to the project directory in your terminal. Then, run the following command: 
```bash
python main.py
```
The screen will display four options: 
1. Client Mode
2. Seeder Mode
3. Split file mode
4. Make torrent file mode

Type in the corresponding option to continue the workflow. For more details on the manual, refer to the **Manual** section of our [Report](https://drive.google.com/file/d/1h4DL5IqhcN2Emrm99tXd2CkrZIf3-cqc/view?usp=sharing)
