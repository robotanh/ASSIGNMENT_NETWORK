import os
import json

def load_json_data(json_path):
    """Load data from the JSON file."""
    with open(json_path, 'r') as file:
        return json.load(file)

def list_files_in_folder(folder_path):
    """List all files in the given folder."""
    return os.listdir(folder_path)

def find_missing_pieces(json_data, folder_path):
    """Identify which pieces are missing in the folder."""
    existing_files = set(list_files_in_folder(folder_path))
    required_pieces = set(json_data['pieces'])
    
    # Find the difference between the required pieces and existing files
    missing_pieces = required_pieces - existing_files
    return missing_pieces

def queue_missing_pieces_for_download(missing_pieces):
    """Queue the missing pieces for download. Implement according to your needs."""
    # This is a placeholder. You might want to implement actual download logic here.
    print("Queueing these pieces for download:", missing_pieces)

def send_missing_pieces():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'torrents', 'ALICE.json')  # Adjust file path
    if not os.path.exists(json_path):
        print("File not found:", json_path)
        return
    folder_path = 'file_split'  # Adjust this path
    
    json_data = load_json_data(json_path)
    missing_pieces = find_missing_pieces(json_data, folder_path)
    if missing_pieces:
        queue_missing_pieces_for_download(missing_pieces)
    else:
        print("All pieces are present in the folder.")


