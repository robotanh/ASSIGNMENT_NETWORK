import os
import json

class TorrentManager:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.torrents_dir = os.path.join(self.current_dir, 'torrents')
        self.torrent_file = self.list_torrent_files()
    
    def get_server_info(self):
        torrentpath = os.path.join(self.torrents_dir,self.torrent_file)
        with open(torrentpath, 'r') as file:
            data = json.load(file)
    
        ip_address = data['ip_address']
        port = data['port']
        
        return ip_address, port

    """
    Return torrent file to use
    """
    def list_torrent_files(self):
        files = [f for f in os.listdir(self.torrents_dir) if f.endswith('.json')]
        if not files:
            print("No torrent files found.")
            return None

        print("Available torrent files:")
        for index, file in enumerate(files, start=1):
            print(f"{index}. {file}")

        try:
            file_index = int(input("Enter the number of the file you want to use: ")) - 1
            if 0 <= file_index < len(files):
                return files[file_index]
            else:
                print("Invalid file number.")
        except ValueError:
            print("Please enter a valid number.")
        return None

    def load_json_data(self, json_path):
        with open(json_path, 'r') as file:
            return json.load(file)

    def list_files_in_folder(self, folder_path):
        return os.listdir(folder_path)

    def find_missing_pieces(self, json_data, folder_path):
        existing_files = set(self.list_files_in_folder(folder_path))
        required_pieces = set(json_data['pieces'])
        missing_pieces = required_pieces - existing_files
        return json.dumps({"file_parts": list(missing_pieces)})

    def queue_missing_pieces_for_download(self, missing_pieces):
        print("Queuing missing pieces for download:", missing_pieces)
        return missing_pieces

    def send_missing_pieces(self):

        if not self.torrent_file:
            return

        json_path = os.path.join(self.torrents_dir, self.torrent_file)
        if not os.path.exists(json_path):
            print("File not found:", json_path)
            return

        folder_path = 'seeder_folder'  # Adjust this path as necessary
        json_data = self.load_json_data(json_path)
        missing_pieces_json = self.find_missing_pieces(json_data, folder_path)
        if missing_pieces_json:
            print("Missing pieces JSON:", missing_pieces_json)
            result = self.queue_missing_pieces_for_download(missing_pieces_json)
            return result
        else:
            print("All pieces are present in the folder.")


    # def send_json_file(self):
    #     torrent_file = self.list_torrent_files()
    #     if not torrent_file:
    #         return

    #     file_path = os.path.join(self.torrents_dir, torrent_file)
    #     if not os.path.exists(file_path):
    #         print("File not found:", file_path)
    #         return

    #     missing_pieces_json = self.send_missing_pieces()
    #     if missing_pieces_json:
    #         print("Missing pieces JSON:", missing_pieces_json)
