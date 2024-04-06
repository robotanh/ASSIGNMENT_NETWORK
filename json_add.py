import os
import json

# Directory containing the files
folder_path = "file_split"

# Get list of filenames in the folder
files = os.listdir(folder_path)

# JSON data to be stored
data = {
    "name_file": "ALICE.txt",
    "ip_address": "192.168.1.3",
    "pieces": files
}

# Path to save JSON file
json_file_path = "output.json"

# Write data to JSON file
with open(json_file_path, "w") as json_file:
    json.dump(data, json_file, indent=4)

print("JSON file has been created successfully.")
