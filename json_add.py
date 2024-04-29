import os
import json

def create_torrent_file( main_file_name, output_file):
    """
    Create a JSON file containing information about the files in the seeder folder.

    :param folder_path: Path to the folder containing the files.
    :param main_file_name: Name of the main file.
    :param ip_address: IP address of the seeder.
    :param port: Port number of the seeder.
    :param output_file: Path to save the JSON file.
    """
    # Get list of filenames in the folder
    ip_address ="192.168.1.3"
    port = 12345
    files = os.listdir("seeder_folder")

    # JSON data to be stored
    data = {
        "name_file": main_file_name,
        "ip_address": ip_address,
        "port": port,
        "pieces": files
    }
    output_file = os.path.join("torrents", output_file)
    # Write data to JSON file
    with open(output_file, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("Torrent file has been created successfully.")

# Example usage:
# create_torrent_file( "ALICE.txt","output.json")
