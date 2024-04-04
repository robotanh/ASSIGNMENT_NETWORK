def split_binary_file(file_path, part_size):
    """
    Splits a binary file into multiple parts of a specified size.

    :param file_path: The path of the file to split.
    :param part_size: The size of each part in bytes.
    """
    with open(file_path, 'rb') as file:
        part_num = 0
        while True:
            data = file.read(part_size)
            if not data:
                break
            part_num += 1
            part_name = f"{file_path}_part{part_num}"
            with open(part_name, 'wb') as part_file:
                part_file.write(data)
            print(f"Created: {part_name}")

def split_text_file(file_path, lines_per_file):
    """
    Splits a text file into multiple parts, each containing a specified
    number of lines.

    :param file_path: The path of the file to split.
    :param lines_per_file: The number of lines each split file should contain.
    """
    with open(file_path, 'r') as file:
        part_num = 0
        lines = []
        for line in file:
            lines.append(line)
            if len(lines) >= lines_per_file:
                part_num += 1
                part_name = f"{file_path}_part{part_num}"
                with open(part_name, 'w') as part_file:
                    part_file.writelines(lines)
                print(f"Created: {part_name}")
                lines = []
        # Save any remaining lines to a final part file
        if lines:
            part_num += 1
            part_name = f"{file_path}_part{part_num}"
            with open(part_name, 'w') as part_file:
                part_file.writelines(lines)
            print(f"Created: {part_name}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python filesplitter.py <file_path> <mode> <size_or_lines>")
        sys.exit(1)

    file_path = sys.argv[1]
    mode = sys.argv[2]
    size_or_lines = int(sys.argv[3])

    if mode == 'binary':
        split_binary_file(file_path, size_or_lines)
    elif mode == 'text':
        split_text_file(file_path, size_or_lines)
    else:
        print("Invalid mode. Use 'binary' or 'text'.")
