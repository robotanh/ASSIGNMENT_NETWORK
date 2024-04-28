
from client import *
from seeder import *
from torrent_action import *
from filesplitter import *
from json_add import *


def show_menu():
    print("Welcome to the Torrent System!")
    print("Select an option:")
    print("1. Client Mode")
    print("2. Seeder Mode")
    print("3. Split file Mode")
    print("4. Make torrent file Mode")

def main():
    show_menu()
    mode = input("Enter the number corresponding to your desired mode: ")

    if mode == "1":
        torrent_manager = TorrentManager()
        host, port = torrent_manager.get_server_info()
        client_mode(host, port, torrent_manager)
    elif mode == "2":
        torrent_manager = TorrentManager()
        host, port = torrent_manager.get_server_info()
        seeder_mode(host, port)
    elif mode == "3":
        print("You have selected Split File Mode.")
        file_path_input = input("Enter the path of the file you want to split: ")
        file_path = file_path_input.strip()

        mode_input = input("Enter the mode you want to split (binary or line): ")
        mode = mode_input.strip().lower()

        if mode == "binary":
            part_size_input = input("Enter the size of each part in bytes: ")
            part_size = int(part_size_input.strip())
            split_binary_file(file_path, part_size)
        elif mode == "line":
            lines_per_file_input = input("Enter the number of lines each split file should contain: ")
            lines_per_file = int(lines_per_file_input.strip())
            split_text_file(file_path, lines_per_file)
        else:
            print("Invalid mode. Please enter 'binary' or 'line'.")

    elif mode == "4":
        file_path_input = input("Enter the file part that you want to create torrent file: ")
        main_file_name = file_path_input
        output_file = input("Enter the output file name: ")
        create_torrent_file(main_file_name, output_file)

if __name__ == "__main__":
    main()
